import {expect,test, type Page} from '@playwright/test';
async function open(page:Page){await page.getByRole('button',{name:'메뉴 열기'}).click();await expect(page.locator('.sidebar')).toBeVisible();await page.waitForTimeout(400);}
for(const viewport of [{width:390,height:480},{width:740,height:360}]){
 test(`작은 메뉴 실제 휠 상하 이동 ${viewport.width}×${viewport.height}`,async({page})=>{
  await page.setViewportSize(viewport);await page.goto('');await open(page);
  const sidebar=page.locator('.sidebar');const box=(await sidebar.boundingBox())!;
  await page.mouse.move(box.x+box.width/2,box.y+box.height/2);await page.mouse.wheel(0,1500);
  await expect.poll(()=>sidebar.evaluate(el=>el.scrollTop)).toBeGreaterThan(0);
  await expect(page.getByRole('button',{name:'데이터 초기화',exact:true})).toBeInViewport();
  await page.getByRole('button',{name:'데이터 초기화',exact:true}).click();await expect(page.getByRole('dialog')).toBeVisible();await page.getByRole('button',{name:'돌아가기',exact:true}).click();
  await page.mouse.move(box.x+box.width/2,box.y+box.height/2);await page.mouse.wheel(0,-1500);
  await expect.poll(()=>sidebar.evaluate(el=>el.scrollTop)).toBe(0);
  await expect(page.getByRole('navigation').getByRole('button',{name:'학습 대시보드',exact:true})).toBeInViewport();
  await page.getByRole('navigation').getByRole('button',{name:'학습 대시보드',exact:true}).click();
  await expect(page.locator('.sidebar')).not.toHaveClass(/open/);
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
 });
}
test('모바일 메뉴 실제 터치 스와이프·글자 확대·높이 변경',async({page,context,isMobile})=>{
 test.skip(!isMobile,'터치 에뮬레이션 프로젝트에서만 실행');
 await page.setViewportSize({width:390,height:480});await page.goto('');
 await page.addStyleTag({content:'.sidebar button {font-size:24px} .sidebar small {font-size:20px}'});
 await open(page);const sidebar=page.locator('.sidebar');const cdp=await context.newCDPSession(page);
 async function swipe(from:number,to:number){
  await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:110,y:from}]});
  for(let i=1;i<=12;i++){await cdp.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:110,y:from+(to-from)*i/12}]});await page.waitForTimeout(20);}
  await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});await page.waitForTimeout(300);
 }
 for(let i=0;i<3;i++)await swipe(400,100);
 await expect.poll(()=>sidebar.evaluate(el=>el.scrollTop)).toBeGreaterThan(0);
 await expect(page.getByRole('button',{name:'데이터 초기화',exact:true})).toBeInViewport();
 const download=page.waitForEvent('download');await page.getByRole('button',{name:/기록 백업/}).click();expect((await download).suggestedFilename()).toMatch(/backup/);
 await page.setViewportSize({width:390,height:420});
 for(let i=0;i<4;i++)await swipe(100,350);
 await expect.poll(()=>sidebar.evaluate(el=>el.scrollTop)).toBe(0);
 await expect(page.getByRole('navigation').getByRole('button',{name:'학습 대시보드',exact:true})).toBeInViewport();
 await page.getByRole('navigation').getByRole('button',{name:'학습 대시보드',exact:true}).click();
});
test('모든 학습 화면에 상단 상태 배너가 없고 저장 실패 경고는 유지',async({page})=>{
 await page.goto('');
 for(const label of ['학습 대시보드','실전 모의시험','랜덤 문제풀이','오답노트','북마크','학습 통계','문제은행 관리']){
  if(await page.getByRole('button',{name:'메뉴 열기'}).isVisible())await open(page);
  await page.getByRole('navigation').getByRole('button',{name:label,exact:true}).click();
  await expect(page.locator('.criteria-note')).toHaveCount(0);await expect(page.getByLabel('학습 기준')).toHaveCount(0);
  if(label!=='문제은행 관리')await expect(page.locator('main')).not.toContainText(/공식 출제기준 대조 대기|잠정 규칙|기출 미제공/);
 }
 await page.addInitScript(()=>{Storage.prototype.setItem=()=>{throw new DOMException('Quota exceeded','QuotaExceededError')}});
 await page.reload();await expect(page.getByRole('alert')).toBeVisible();
});
