import { describe, expect, it } from 'vitest';
import {execFileSync} from 'node:child_process';
import {readFileSync} from 'node:fs';
import {BASE_BANK as bank, createExam, grade, SUBJECTS, fingerprint, validateQuestion, emptyStore, answerExam, submitExam, restoreStore, remainingSeconds} from '../src/model';
import {EXAM} from '../src/config';
// Independent equations: these do not import the generator or its computed answers.
const equations:Record<string,(v:number[])=>number>={
 fieldForce:([e,q])=>q/1e6*e*1000,
 capCharge:([c,u])=>c/1e6*u*1000,
 capEnergy:([c,u])=>c/1e6*u*u/2,
 flux:([b,a])=>b*(a/10000)*1000,
 solenoid:([n,i])=>n*i*2,
 lineLoss:([r,i])=>r*i*i+r*i*i+r*i*i,
 transmissionEfficiency:([input,output])=>output/(input/100),
 loadFactor:([max,avg])=>avg/max*100,
 demandFactor:([capacity,max])=>max/capacity*100,
 compensation:([_p,q])=>q-10,
 turns:([n,u])=>u/(n/100),
 syncSpeed:([f,p])=>60*f/(p/2),
 slip:([ns,n])=>(1-n/ns)*100,
 machineEfficiency:([input,output])=>100-(input-output)/input*100,
 torque:([p,n])=>9550/(n/p),
 impedance:([r,x])=>Math.hypot(r,x),
 rlCurrent:([u])=>u/Math.hypot(3,4),
 timeConstant:([r,c])=>r*1000*c/1e6*1000,
 parallelR:([a,b])=>1/(1/a+1/b),
 acPower:([u,i])=>u*(i*0.8),
 illuminance:([i,r])=>i/(r*r),
 averageIlluminance:([flux,area])=>flux*(10/area)*(0.5*0.8),
 conductorR:([length,area])=>(length/area)/50,
 energy:([p,t])=>p*t,
 diversity:([sum,max])=>sum/max,
};
describe('새 문제은행 내부 검수',()=>{
 it('실등록 1000 · 25유형 · 과목별 200 · 목표 부족 0을 숨기지 않는다',()=>{
  expect(bank).toHaveLength(1000);expect(1000-bank.length).toBe(0);
  expect(new Set(bank.map(q=>q.family)).size).toBe(25);
  SUBJECTS.forEach(s=>expect(bank.filter(q=>q.subject===s)).toHaveLength(200));
  expect(new Set(bank.map(q=>q.id)).size).toBe(bank.length);
  expect(new Set(bank.map(fingerprint)).size).toBe(bank.length);
  bank.forEach(q=>{expect(validateQuestion(q)).toEqual(q);expect(q.type).toBe('original');expect(q.year).toBeNull();expect(q.session).toBeNull();expect(q.verificationStatus).toBe('reviewed');});
 });
 it('원고 재생성이 바이트 단위로 같다',()=>{
  const before=readFileSync('src/data/questions-main.json','utf8');
  execFileSync('python',['scripts/generate_bank.py']);
  expect(readFileSync('src/data/questions-main.json','utf8')).toBe(before);
 });
 for(const q of bank) it(`독립 식·정답 위치·단위·보기 유일성 ${q.id}`,()=>{
  const c=q.calculation!; const actual=equations[c.kind](c.values);
  expect(c.result).toBeCloseTo(actual,3);
  expect(Number.parseFloat(q.choices[q.answer-1])).toBeCloseTo(actual,3);
  expect(q.choices.filter(choice=>Math.abs(Number.parseFloat(choice)-actual)<0.0005)).toHaveLength(1);
  q.choices.forEach(choice=>expect(choice.slice(String(Number.parseFloat(choice)).length).trim()).toBe(c.unit));
  expect(q.explanation).toContain(String(c.result));expect(q.explanation).not.toMatch(/undefined|NaN|\{[abr]\}/);
 });
});
describe('전기산업기사 학습용 시험 설정',()=>{
 it('5과목 각20개, 고유100개, 150분; 부족·검증대기는 차단',()=>{
  const e=createExam(bank,'main',1000);
  expect(e.questions).toHaveLength(100);expect(new Set(e.questions.map(q=>q.id)).size).toBe(100);
  SUBJECTS.forEach(s=>expect(e.questions.filter(q=>q.subject===s)).toHaveLength(20));
  expect(e.deadline-e.startedAt).toBe(150*60000);
  expect(()=>createExam(bank.filter(q=>q.subject!==SUBJECTS[0]),'main')).toThrow();
  expect(()=>createExam(bank.map(q=>q.subject===SUBJECTS[0]?{...q,verificationStatus:'pending'}:q),'main')).toThrow();
 });
 function answered(counts:number[]){const e=createExam(bank,'main');SUBJECTS.forEach((s,i)=>e.questions.filter(q=>q.subject===s).slice(0,counts[i]).forEach(q=>e.answers[q.id]=q.answer));return e;}
 it('59점 실패,60점 합격; 40점 과락 경계는 포함',()=>{
  expect(grade(answered([11,12,12,12,12])).passed).toBe(false);
  expect(grade(answered([12,12,12,12,12]))).toMatchObject({score:60,passed:true,correct:60,unanswered:40});
  expect(grade(answered([8,13,13,13,13])).passed).toBe(true);
  expect(grade(answered([7,20,20,20,20]))).toMatchObject({score:87,passed:false});
 });
 it('답안 변경·만료 차단·중복 제출·새로고침 복원',()=>{
  let s={...emptyStore(),exam:createExam(bank,'main',1000)};const q=s.exam.questions[0];
  let state=answerExam(s,q.id,1,2000);state=answerExam(state,q.id,2,3000);
  expect(state.exam?.answers[q.id]).toBe(2);
  const restored=restoreStore(JSON.stringify(state));expect(restored).toEqual(state);
  expect(remainingSeconds(restored.exam!.deadline,1000)).toBe(9000);
  state=answerExam(state,q.id,3,9001000);expect(state.exam).toBeNull();expect(state.results[0].answers[q.id]).toBe(2);
  expect(state.results[0].reason).toBe('timeout');expect(state.attempts).toHaveLength(100);expect(submitExam(state)).toEqual(state);
 });
 it('저장된 시험의 과목 분포 손상은 거부',()=>{
  const s={...emptyStore(),exam:createExam(bank,'main',1000)};s.exam.questions[0]={...s.exam.questions[0],subject:'가짜과목'};expect(()=>restoreStore(JSON.stringify(s))).toThrow();
 });
});
describe('검수·배포 계약 회귀',()=>{
 it('변형별 입력이 고유하고 수치 조건이 물리적 범위 안에 있다',()=>{
  for(const family of new Set(bank.map(q=>q.family))){const items=bank.filter(q=>q.family===family);expect(items).toHaveLength(40);expect(new Set(items.map(q=>JSON.stringify(q.calculation!.values))).size).toBe(40);}
  for(const q of bank){const c=q.calculation!;expect(c.values.every(v=>Number.isFinite(v)&&v>0)).toBe(true);expect(c.result).toBeGreaterThan(0);if(['transmissionEfficiency','machineEfficiency','loadFactor','demandFactor','slip'].includes(c.kind))expect(c.result).toBeLessThanOrEqual(100);}
 });
 it('Pages 배포는 수동 이벤트만 있고 push CI에는 배포 동작이 없다',()=>{
  const pages=readFileSync('.github/workflows/pages.yml','utf8'),ci=readFileSync('.github/workflows/ci.yml','utf8');
  expect(pages).toContain('workflow_dispatch:');expect(pages).not.toMatch(/^  (push|pull_request|workflow_run|schedule|repository_dispatch):/m);
  expect(pages).toContain("github.event_name == 'workflow_dispatch'");expect(pages).toContain('needs: validate');
  expect(ci).not.toMatch(/deploy-pages|configure-pages|pages: write|id-token: write/);
 });
});
