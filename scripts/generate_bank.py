"""Deterministic, newly authored practice bank. No past-exam source is claimed."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SUBJECTS=['전기자기학','전력공학','전기기기','회로이론','전기설비기술기준']
# Templates are the authored manuscript. Values vary by k=1..40, not by random seed.
FAMILIES=[
(0,'fieldForce','전계와 힘','균일한 전계의 세기가 {a} N/C이고 양전하가 {b} μC이다. 전하에 작용하는 힘의 크기는 몇 mN인가?',lambda k:(100*k,20),'mN',lambda a,b:a*b/1000,'F=qE, q={b}×10⁻⁶ C. F={a}×{b}×10⁻⁶ N={r} mN. 양전하의 힘은 전계 방향이다.'),
(0,'capCharge','정전용량','이상적인 {a} μF 커패시터에 {b} V를 인가했다. 저장 전하량은 몇 mC인가?',lambda k:(20*k,100),'mC',lambda a,b:a*b/1000,'Q=CV. C={a}×10⁻⁶ F이므로 Q={a}×10⁻⁶×{b} C={r} mC.'),
(0,'capEnergy','전계 에너지','이상적인 {a} μF 커패시터의 전압이 {b} V이다. 저장 에너지는 몇 J인가?',lambda k:(200*k,100),'J',lambda a,b:a*b*b/2000000,'W=CV²/2. C={a}×10⁻⁶ F를 대입하면 W={a}×10⁻⁶×{b}²/2={r} J.'),
(0,'flux','자속','균일한 자속밀도 {a} T가 면적 {b} cm²인 평면에 수직으로 통과한다. 자속은 몇 mWb인가?',lambda k:(k,20),'mWb',lambda a,b:a*b/10,'Φ=BA. 면적 A={b}×10⁻⁴ m². Φ={a}×{b}×10⁻⁴ Wb={r} mWb. 평면에 수직이므로 각도 인자는 1이다.'),
(0,'solenoid','자계 세기','누설과 단부 효과를 무시한 긴 솔레노이드의 권수가 {a}회, 전류가 {b} A, 길이가 0.5 m이다. 내부 자계 세기 H는 몇 A/m인가?',lambda k:(100*k,2),'A/m',lambda a,b:a*b/0.5,'암페어 법칙 Hℓ=NI. H=NI/ℓ={a}×{b}/0.5={r} A/m. 자속밀도 B와 구별한다.'),
(1,'lineLoss','송전 손실','평형 3상 선로에서 각 선의 저항이 {a} Ω, 선전류가 {b} A이다. 저항에 의한 전체 유효전력 손실은 몇 W인가?',lambda k:(k,10),'W',lambda a,b:3*a*b*b,'각 선 손실은 I²R이며 3개 선이므로 P손=3I²R=3×{b}²×{a}={r} W. 저항은 한 선의 값이다.'),
(1,'transmissionEfficiency','송전 효율','송전단 유효전력이 {a} kW, 수전단 유효전력이 {b} kW이다. 송전 효율은 몇 %인가?',lambda k:(100,70+k/2),'%',lambda a,b:100*b/a,'η=수전단 전력/송전단 전력×100={b}/{a}×100={r} %. 양쪽은 같은 시간의 유효전력이다.'),
(1,'loadFactor','부하율','하루 최대수요전력이 {a} kW, 같은 날 평균전력이 {b} kW이다. 일 부하율은 몇 %인가?',lambda k:(100,30+k),'%',lambda a,b:100*b/a,'부하율=동일 기간 평균전력/최대수요전력×100={b}/{a}×100={r} %. 설비용량을 분모로 하는 수용률과 다르다.'),
(1,'demandFactor','수용률','설비용량 합계가 {a} kW, 최대수요전력이 {b} kW이다. 수용률은 몇 %인가?',lambda k:(200,60+2*k),'%',lambda a,b:100*b/a,'수용률=최대수요전력/설비용량×100={b}/{a}×100={r} %. 기간 평균전력을 사용하지 않는다.'),
(1,'compensation','무효전력 보상','유효전력 {a} kW인 부하의 지상 무효전력이 보상 전 {b} kvar, 보상 후 10 kvar이다. 이상적인 병렬 콘덴서가 공급할 용량성 무효전력 크기는 몇 kvar인가?',lambda k:(100,20+10*k),'kvar',lambda a,b:b-10,'유효전력 {a} kW는 보상으로 변하지 않는다고 가정한다. Qc=Q전−Q후={b}−10={r} kvar. 손실과 고조파는 무시한다.'),
(2,'turns','변압기','이상적인 단상 변압기의 1차 권수 {a}회, 2차 권수 100회, 1차 전압 {b} V이다. 2차 전압은 몇 V인가?',lambda k:(100*k,200*k),'V',lambda a,b:b*100/a,'이상적인 변압기 V₂/V₁=N₂/N₁. V₂={b}×100/{a}={r} V. 부하 전압강하와 손실은 무시한다.'),
(2,'syncSpeed','동기속도','주파수 {a} Hz, 극수 {b}인 교류기의 동기속도는 몇 r/min인가?',lambda k:(50+10*k,4),'r/min',lambda a,b:120*a/b,'nₛ=120f/P. P는 극쌍 수가 아닌 전체 극수이다. nₛ=120×{a}/{b}={r} r/min.'),
(2,'slip','유도전동기','동기속도 {a} r/min인 유도전동기의 회전자 속도가 {b} r/min이다. 슬립은 몇 %인가?',lambda k:(1500,1500-15*k),'%',lambda a,b:100*(a-b)/a,'s=(nₛ−n)/nₛ. s=({a}−{b})/{a}×100={r} %. 전동기 운전이며 회전자는 동기속도보다 느리다.'),
(2,'machineEfficiency','효율','전동기의 전기 입력이 {a} kW, 축 출력이 {b} kW이다. 효율은 몇 %인가?',lambda k:(100,75+k/2),'%',lambda a,b:100*b/a,'η=축 출력/전기 입력×100={b}/{a}×100={r} %. 입력과 출력 모두 유효전력이며 손실은 그 차이다.'),
(2,'torque','축 토크','축 출력 {a} kW, 회전속도 {b} r/min인 전동기의 토크는 몇 N·m인가? 근사식 T=9550P/n을 사용한다.',lambda k:(k,1000),'N·m',lambda a,b:9550*a/b,'P=Tω와 ω=2πn/60으로부터 kW를 W로 바꾸면 T≈9550P/n. 지정한 근사상수로 T=9550×{a}/{b}={r} N·m.'),
(3,'impedance','RL 직렬','저항 {a} Ω과 유도 리액턴스 {b} Ω이 직렬인 회로의 임피던스 크기는 몇 Ω인가?',lambda k:(3*k,4*k),'Ω',lambda a,b:(a*a+b*b)**0.5,'Z=R+jX이므로 |Z|=√(R²+X²)=√({a}²+{b}²)={r} Ω. 저항과 리액턴스를 산술 합산하지 않는다.'),
(3,'rlCurrent','교류 전류','저항 3 Ω과 유도 리액턴스 4 Ω의 직렬 회로에 실효값 {a} V를 인가한다. 전류 실효값은 몇 A인가? 두 번째 조건값 {b}는 전원 주파수(Hz)이며 리액턴스는 이 주파수에서의 값이다.',lambda k:(50*k,60),'A',lambda a,b:a/5,'주파수 {b} Hz에서 |Z|=√(3²+4²)=5 Ω. 실효값 옴의 법칙 I=V/|Z|={a}/5={r} A.'),
(3,'timeConstant','RC 시정수','저항 {a} kΩ과 커패시터 {b} μF로 구성한 1차 RC 회로의 시정수는 몇 ms인가?',lambda k:(10*k,2),'ms',lambda a,b:a*b,'τ=RC. τ={a}×10³×{b}×10⁻⁶ s={r} ms. 시정수는 최종값에 도달하는 총 시간이 아니다.'),
(3,'parallelR','병렬 저항','저항 {a} Ω과 {b} Ω을 병렬 연결한다. 합성저항은 몇 Ω인가?',lambda k:(6*k,3*k),'Ω',lambda a,b:a*b/(a+b),'병렬 합성저항 R=R₁R₂/(R₁+R₂)={a}×{b}/({a}+{b})={r} Ω. 어느 개별 저항보다 작다.'),
(3,'acPower','단상 유효전력','단상 부하의 전압 실효값 {a} V, 전류 실효값 {b} A, 역률 0.8이다. 유효전력은 몇 W인가?',lambda k:(100*k,5),'W',lambda a,b:a*b*0.8,'정현파 단상 유효전력 P=VI cosφ={a}×{b}×0.8={r} W. 피상전력 VI와 구별한다.'),
(4,'illuminance','조명 기초','점광원의 해당 방향 광도가 {a} cd이다. 광원에서 {b} m 떨어진 수직 입사면의 조도는 몇 lx인가? 반사광은 무시한다.',lambda k:(100*k,2),'lx',lambda a,b:a/b**2,'거리 역제곱 법칙 E=I/r². 수직 입사이므로 cosθ=1. E={a}/{b}²={r} lx. 법령상 최저 조도 기준을 묻는 문항이 아니다.'),
(4,'averageIlluminance','조명 설계','한 실에 등기구 10개가 있고 각 등기구 광속이 {a} lm이다. 이용률 0.5, 보수율 0.8, 바닥 면적 {b} m²일 때 평균조도는 몇 lx인가?',lambda k:(1000*k,100),'lx',lambda a,b:10*a*0.5*0.8/b,'광속법 E=NΦUM/A. E=10×{a}×0.5×0.8/{b}={r} lx. 이용률·보수율은 주어진 설계 조건이며 법정값이 아니다.'),
(4,'conductorR','전선 저항','도체의 고유저항을 0.02 Ω·mm²/m로 일정하다고 가정한다. 한 가닥 길이 {a} m, 단면적 {b} mm²일 때 저항은 몇 Ω인가? 접속저항은 무시한다.',lambda k:(100*k,2),'Ω',lambda a,b:0.02*a/b,'R=ρℓ/A. 주어진 고유저항은 가정값이다. R=0.02×{a}/{b}={r} Ω. 왕복 길이를 추가하지 않는 한 가닥 계산이다.'),
(4,'energy','전력량','유효전력이 일정한 {a} kW 부하를 {b}시간 사용한다. 소비 전력량은 몇 kWh인가?',lambda k:(2*k,5),'kWh',lambda a,b:a*b,'W=Pt={a}×{b}={r} kWh. 요금제·법정 설비 기준을 가정하지 않는다. 전력(kW)과 에너지(kWh)를 구별한다.'),
(4,'diversity','부등률','여러 부하의 개별 최대수요전력 합이 {a} kW, 부하군 전체의 합성 최대수요전력이 {b} kW이다. 부등률은 얼마인가?',lambda k:(120+20*k,100),'',lambda a,b:a/b,'부등률=개별 최대수요전력 합/합성 최대수요전력={a}/{b}={r}. 무차원 비율이며 퍼센트 수용률과 다르다.'),
]
def fmt(x):return f'{x:.3f}'.rstrip('0').rstrip('.') if x%1 else str(int(x))
def generate():
 out=[]
 for n,(subject,kind,topic,stem,inputs,unit,formula,explanation) in enumerate(FAMILIES):
  for k in range(1,41):
   a,b=inputs(k);result=round(formula(a,b),3);r=fmt(result)
   nums=[result,result+1,result+2,result+3];shift=(n+k)%4;nums=nums[shift:]+nums[:shift];answer=nums.index(result)+1
   out.append(dict(id=f'IEE-{n+1:02d}-{k:02d}',subject=SUBJECTS[subject],topic=topic,question=stem.format(a=fmt(a),b=fmt(b)),choices=[f'{fmt(x)} {unit}'.strip() for x in nums],answer=answer,explanation=explanation.format(a=fmt(a),b=fmt(b),r=r),difficulty='중',year=None,session=None,type='original',sourceUrl='https://github.com/YunSangYeong/Industrial-Engineer-Electricity-CBT/blob/codex/electricity-cbt-20261021/docs/question-review.md',verificationStatus='reviewed',reviewNote='AI 일반 지식으로 신규 작성. 식·조건·단위·정답·해설 문장 내부 검토 및 독립 계산 테스트. 공식 출제기준 대조·전문가 검수 미실시. 전기설비기술기준 문항은 규정 수치가 아닌 설비 계산 기초만 포함.',version='main',rights='CC BY 4.0 · Industrial-Engineer-Electricity-CBT contributors · AI 보조 자체 제작',family=f'IEE-{kind}',calculation=dict(kind=kind,values=[a,b],result=result,unit=unit,precision=3)))
 return out
if __name__=='__main__':
 text=json.dumps(generate(),ensure_ascii=False,indent=2)+'\n'
 (ROOT/'src/data/questions-main.json').write_text(text)
 print('1000 original questions; 25 families × 40 variants. Target shortage: 0.')
