import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from urllib.parse import quote, urljoin

# 데이터 프레임을 만들기 위한 딕셔너리
DB={
    'Exercise name':[],
    'Exercise details':[], 
    'Starting position':[], 
    'Execution':[], 
    'Comments and tips':[],
    'image_url':[],
    'video_url':[]
}

def Save_to_DB():
    # 이미지 정보 저장
    #운동 이미지를 찾아 image에 저장
    wait = WebDriverWait(driver, 10)
    image = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.post-top-featured.wp-post-image')))

    #이미지의 src 속성 가져오기
    image_url = image.get_attribute("src")
    #DB 리스트에 저장
    DB['image_url'].append(image_url)

    # 운동 정보 저장
    #운동 이름을 찾아서 텍스트 가져오기
    content_element = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/article/div/header/h1')
    #DB 리스트에 저장
    DB['Exercise name'].append(content_element.text)

    #운동 상세 정보를 찾아서 텍스트 가져오기
    content_element = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/article/div/div/div/ul[1]')
    Exercise_details = content_element.text
    DB["Exercise details"].append(Exercise_details)

    try:
        content_element = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/article/div/div/div/ol[1]')
    except NoSuchElementException:
        #NoSuchElementException 예외처리
        try:
            content_element = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/article/div/div/div/p[1]')
        except NoSuchElementException:
            #NoSuchElementException 예외처리
            content_element = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/article/div/div/div/ul[2]')
        finally:
            pass
    finally:
        Starting_position = content_element.text
        pass

    #예외처리
    if(Starting_position=='''Exhale as you push the barbell straight upward.
    At the top of the movement, shrug your shoulders to raise the barbell even higher.
    Inhale as you reverse the motions and lower the barbell to the starting position in a controlled manner.
    Repeat.'''):
        content_element = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/article/div/div/div/p')
        Starting_position = content_element.text

    #DB 리스트에 저장
    DB["Starting position"].append(Starting_position)

    try:
        content_element = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/article/div/div/div/ol[2]')
    except NoSuchElementException:
        #NoSuchElementException 예외처리
        content_element = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/article/div/div/div/ul[2]')
    finally:
        Execution = content_element.text
        if(Execution=='Do not lock your elbows out.\nMove your head out of the way of the bar by rocking your body slightly forward as the bar ascends and slightly backward as the bar descends.\nKeep your back straight and head facing forward; don’t look up.\nContract your core to stabilize your torso.\nKeep your elbows a little forward, not directly out to the sides.\nOverhead presses are great for building functional upper-body strength. The seated barbell shoulder press variation takes your legs out of the equation, which better isolates your shoulders and reduces your potential to cheat.\nIf lifting very heavy, use a bench with a back support and rack. The angle of the back support should be a little less than vertical.\nSee also the standing wide-grip barbell overhead press, the band shoulder press, the Smith machine shoulder press, and the seated dumbbell one-arm shoulder press.'):
            content_element = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/article/div/div/div/ol')
            Execution = content_element.text
        pass

    #예외처리
    if(Execution=='''Behind-the-neck pull-up
    Behind-the-neck shoulder press'''):
        content_element = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/article/div/div/div/p[2]')
        Execution = content_element.text

    content_element = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/article/div/div/div/ul[2]')
    Comments_and_tips=content_element.text

    #예외처리
    if(Starting_position==Execution):
        content_element = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/article/div/div/div/ul[3]')
        Execution = content_element.text
        if(Starting_position==Comments_and_tips):
            content_element = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/article/div/div/div/ul[4]')
            Comments_and_tips=content_element.text

    #예외처리
    if(Execution==Comments_and_tips):
        try:
            content_element = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/article/div/div/div/ul[3]')
            Comments_and_tips=content_element.text
            #예외처리
            if(Comments_and_tips=='ExRx.net, Barbell Shoulder Press'):
                content_element = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/article/div/div/div/ul[2]')
                Execution = content_element.text
        except NoSuchElementException:
            #NoSuchElementException 예외처리
            try:
                a = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/article/div/div/div/p[2]')
                b = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/article/div/div/div/p[3]')
                c = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/article/div/div/div/p[4]')
                Execution = a.text
                Comments_and_tips = '\n'.join([b.text, c.text])
            except NoSuchElementException:
                pass
        # 예외 처리 이후의 공통 부분
        finally:
            pass
    
    #예외처리
    if(Comments_and_tips=='''Behind-the-neck pull-up
    Behind-the-neck shoulder press'''):
        a = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/article/div/div/div/p[3]')
        b = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/article/div/div/div/h3[1]')
        c = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/article/div/div/div/p[4]')
        d = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/article/div/div/div/h3[2]')
        e = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/article/div/div/div/p[5]')
        f = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/article/div/div/div/h3[3]')
        g = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/article/div/div/div/ul[2]')
        Comments_and_tips = '\n'.join([a.text, b.text, c.text, d.text, e.text, f.text, g.text])

    #DB 리스트에 저장
    DB["Execution"].append(Execution)
    DB["Comments and tips"].append(Comments_and_tips)

    # 동영상 정보 저장
    #동영상 개수 확인
    iframe_element = driver.find_elements(By.XPATH, '/html/body/div[1]/div/div/div/main/div/article/div/div/div/figure')
    iframe_num=len(iframe_element)

    #임시 저장 변수 생성
    temp_video_url = None  # 초기값은 None으로 설정

    if(iframe_num==0):
        xpath=''
        a = '/html/body/div[1]/div/div/div/main/div/article/div/div/div/div[2]/iframe'
        b = '/html/body/div[1]/div/div/div/main/div/article/div/div/div/figure/div/iframe'
        c = '/html/body/div[1]/div/div/div/main/div/article/div/div/div/p[1]/iframe'
        d = '/html/body/div[1]/div/div/div/main/div/article/div/div/div/p'

        #a ~ d까지 순차적으로 element가 있는지 확인
        if len(driver.find_elements(By.XPATH, a)) > 0:
            iframe_element = driver.find_elements(By.XPATH, a)
            xpath=a
        elif len(driver.find_elements(By.XPATH, b)) > 0:
            iframe_element = driver.find_elements(By.XPATH, b)
            xpath=b
        elif len(driver.find_elements(By.XPATH, c)) > 0:
            iframe_element = driver.find_elements(By.XPATH, c)
            xpath=c
        elif len(driver.find_elements(By.XPATH, d)) > 0:
            temp_video_url = driver.find_element(By.XPATH, d).text
        else:
            temp_video_url=[]

        for index, iframe in enumerate(iframe_element):
            #동영상 정보를 찾아 iframe_element에 저장
            try:
                wait = WebDriverWait(driver, 10)
                iframe_element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

                # 동영상 URL 가져오기
                if iframe_num == 1:
                    temp_video_url = iframe_element.get_attribute('data-ezsrc')  # 단일 동영상이면 문자열로 설정
                else:
                    if temp_video_url is None:
                        temp_video_url = []  # 여러 개의 동영상이고, 초기값이 None이면 빈 리스트로 초기화
                    temp_video_url.append(iframe_element.get_attribute('data-ezsrc'))  # 리스트에 추가
            except TimeoutException:
                # 대기 시간이 초과되면 해당 요소가 없다고 간주하고 빈 리스트로 초기화
                temp_video_url = []
    else:
        #동영상 개수 만큼 반복
        for index, iframe in enumerate(iframe_element):
            #동영상 정보를 찾아 iframe_element에 저장
            try:
                wait = WebDriverWait(driver, 10)
                iframe_element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/main/div/article/div/div/div/figure['+str(index+1)+']/div/iframe')))

                # 동영상 URL 가져오기
                if iframe_num == 1:
                    temp_video_url = iframe_element.get_attribute('data-ezsrc')  # 단일 동영상이면 문자열로 설정
                else:
                    if temp_video_url is None:
                        temp_video_url = []  # 여러 개의 동영상이고, 초기값이 None이면 빈 리스트로 초기화
                    temp_video_url.append(iframe_element.get_attribute('data-ezsrc'))  # 리스트에 추가
            except TimeoutException:
                # 대기 시간이 초과되면 해당 요소가 없다고 간주하고 빈 리스트로 초기화
                temp_video_url = []
    #DB 리스트에 저장
    DB['video_url'].append(temp_video_url)



# 웹 드라이버 시작
driver = webdriver.Chrome()

action = ActionChains(driver)

# 페이지 1 ~ 44까지 반복
for page in range(1,45):
    url = 'https://weighttraining.guide/exercises/page/'+str(page)+'/'
    driver.get(url)

    # 운동명 저장 변수 선언
    content_element=[]
    # 운동명을 찾아서 텍스트 가져오기
    for i in range(1,13):
        content_element.append(driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/article['+str(i)+']/div/header/h2').text)
        # page가 44면 1번만 반복함
        if page == 44:
            break

    for index, content in enumerate(content_element):
        # 운동 이름과 주소값이 다른경우 예외처리
        if(content=="Dumbbell sumo squat (version 2)"):
            content="Dumbbell sumo squat 2"
        if(content=="Captain’s chair straight leg raise"):
            content="Captains chair straight leg raise"
        if(content=="Dumbbell farmer’s walk"):
            content="Dumbbell farmers walk"
        if(content=="Smith machine wide-grip upright row"):
            content="Smith machine upright row"
        if(content=="Trap bar farmer’s walk"):
            content="Trap-bar farmers walk"
        if(content=="Captain’s chair leg raise"):
            content="Captains chair leg raise"
        if(content=="Weighted captain’s chair leg and hip raise"):
            content="Weighted captains chair leg and hip raise"
        if(content=="Side-lying reverse dumbbell fly"):
            content="Side lying dumbbell rear delt raise"
        if(content=="One-arm reverse dumbbell fly"):
            content="One arm dumbbell bent over lateral raise"
        if(content=="Seated behind-the-neck barbell shoulder press"):
            content="Behind the neck barbell overhead press"
        if(content=="Seated elbows-in dumbbell overhead press"):
            content="Seated neutral grip dumbbell overhead press"
        if(content=="Lying alternating straight leg raise"):
            content="Lying alternating leg raise"
        if(content=="Seated overhead EZ bar triceps extension"):
            content='Overhead ez bar triceps extension'
        if(content=="Captain’s chair leg and hip raise"):
            content="Captains chair leg and hip raise"
        if(content=="Machine-assisted pull-up"):
            content="Assisted pull up"
        if(content=="Smith machine chair squat"):
            content="Smith chair squat"
        if(content=="Lying one-arm reverse dumbbell fly"):
            content="Lying dumbbell one arm rear lateral raise"
        if(content=="Decline barbell skull crusher"):
            content="Decline skull crusher"
        if(content=="Seated leg raise"):
            content="Seated knee raise"
        if(content=="Single leg glute bridge"):
            content="Single leg hip thrust"
        if(content=="Hanging leg and hip raise"):
            content="Hanging leg-hip raise"
        if(content=="Lying leg and hip raise"):
            content="Lying leg hip raise"
        if(content=="Dumbbell one-arm shoulder press"):
            content="Dumbbell one arm overhead press"
        if(content=="Dumbbell cross-body hammer curl"):
            content="Cross body hammer curl"
        if(content=="Barbell shoulder press"):
            content="Barbell overhead press"
        if(content=="Machine seated calf raise"):
            content="Seated calf raise"
        if(content=="Hanging straight leg and hip raise"):
            content="Hanging straight leg hip raise"
        if(content=="Triceps rope push-down"):
            content="Triceps push down"
        if(content=="Standing incline cable fly"):
            content="Low cable cross over"
        if(content=="Standing cable fly"):
            content="Cable cross over"
        if(content=="Barbell bench press"):
            content="Bench press"
        if(content=="Reverse dumbbell fly"):
            content="Bent over lateral raise"
        if(content=="Dumbbell kickback"):
            content="Triceps dumbbell kickback"
        if(content=="Incline straight leg and hip raise"):
            content="Incline straight leg hip raise"
        if(content=="Dumbbell lateral raise"):
            content="Lateral raise"
        if(content=="Dumbbell concentration curl"):
            content="Concentration curl"
        
        # 운동명을 실제 주소값으로 변환
        encoded_content = quote(content.replace(" ", "-"), safe='()')
        url = urljoin('https://weighttraining.guide/exercises/', encoded_content + '/')
        # 해당 운동명의 상세페이지로 이동
        driver.get(url)

        # 운동 정보 DB에 저장
        Save_to_DB()
        
# 브라우저 종료
driver.quit()

# 데이터를 Pandas 데이터프레임으로 변환
df = pd.DataFrame(DB)

# 데이터프레임 출력
print(df)

#csv파일 형태로 출력
df.to_csv("weighttraining.guide.csv", encoding='utf-8-sig')