import os
import pygame
pygame.init()

# 화면 크기 설정
screen_width = 640 # 가로 크기
screen_height = 480 # 세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("Nado Pang")

# FPS
clock = pygame.time.Clock()

# 1. 사용자 게임 초기화 (배경 화면, 게임 이미지, 좌표, 속도, 폰트 등)
current_path = os.path.dirname(__file__) # 현재 파일의 위치 반환
image_path = os.path.join(current_path, "images") # images 폴더 위치 반환

# 배경 만들기
background = pygame.image.load(os.path.join(image_path, "background.png"))

# 스테이지 만들기
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1] 

# 캐릭터 만들기
character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - character_height - stage_height

# 캐릭터 이동 방향
character_to_x = 0

# 캐릭터 이동 속도
character_speed = 5

# 무기 만들기
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

# 무기는 한 번에 여러 발 발사 가능
weapons = []

# 무기 이동 속도
weapon_speed = 10

# 장애물 만들기 
star_images = [
    pygame.image.load(os.path.join(image_path, "star1.png")),
    pygame.image.load(os.path.join(image_path, "star2.png")),
    pygame.image.load(os.path.join(image_path, "star3.png")),
    pygame.image.load(os.path.join(image_path, "star4.png"))]

# 장애물 크기에 따른 최초 스피드
star_speed_y = [-18, -15, -12, -9] # index 0, 1, 2, 3 에 해당하는 값

# 장애물들
stars = []

# 최초 발생하는 큰 장애물 추가
stars.append({
    "pos_x" : 50, # 공의 x 좌표
    "pos_y" : 50, # 공의 y 좌표
    "img_idx" : 0, # 공의 이미지 인덱스
    "to_x": 3, # x축 이동방향, -3 이면 왼쪽으로, 3 이면 오른쪽으로
    "to_y": -6, # y축 이동방향,
    "init_spd_y": star_speed_y[0]})# y 최초 속도

# 사라질 무기, 장애물 정보 저장 변수
weapon_to_remove = -1
star_to_remove = -1

# Font 정의
game_font = pygame.font.Font(None, 40)
total_time = 100
start_ticks = pygame.time.get_ticks() # 시작 시간 정의

# 게임 종료 메시지 
# Time Over(시간 초과 실패)
# Mission Complete(성공)
# Game Over (캐릭터 장애물에 맞음, 실패)
game_result = "Game Over"

running = True
while running:
    dt = clock.tick(30)
    
    # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: # 캐릭터를 왼쪽으로
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT: # 캐릭터를 오른쪽으로
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE: # 무기 발사
                weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0

    # 3. 게임 캐릭터 위치 정의
    character_x_pos += character_to_x

    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    # 무기 위치 조정
    # 100, 200 -> 180, 160, 140, ...
    # 500, 200 -> 180, 160, 140, ...
    weapons = [ [w[0], w[1] - weapon_speed] for w in weapons] # 무기 위치를 위로

    # 천장에 닿은 무기 없애기
    weapons = [ [w[0], w[1]] for w in weapons if w[1] > 0]
    
    # 장애물 위치 정의
    for star_idx, star_val in enumerate(stars):
        star_pos_x = star_val["pos_x"]
        star_pos_y = star_val["pos_y"]
        star_img_idx = star_val["img_idx"]

        star_size = star_images[star_img_idx].get_rect().size
        star_width = star_size[0]
        star_height = star_size[1]

        # 가로벽에 닿았을 때 장애물 이동 위치 변경 (튕겨 나오는 효과)
        if star_pos_x < 0 or star_pos_x > screen_width - star_width:
            star_val["to_x"] = star_val["to_x"] * -1

        # 세로 위치
        # 스테이지에 튕겨서 올라가는 처리
        if star_pos_y >= screen_height - stage_height - star_height:
            star_val["to_y"] = star_val["init_spd_y"]
        else: # 그 외의 모든 경우에는 속도를 증가
            star_val["to_y"] += 0.5

        star_val["pos_x"] += star_val["to_x"]
        star_val["pos_y"] += star_val["to_y"]

    # 4. 충돌 처리

    # 거북이 rect 정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for star_idx, star_val in enumerate(stars):
        star_pos_x = star_val["pos_x"]
        star_pos_y = star_val["pos_y"]
        star_img_idx = star_val["img_idx"]

        # 장애물 rect 정보 업데이트
        star_rect = star_images[star_img_idx].get_rect()
        star_rect.left = star_pos_x
        star_rect.top = star_pos_y

        # 장애물과 캐릭터 충돌 체크
        if character_rect.colliderect(star_rect):
            running = False
            break

        # 장애물과 무기들 충돌 처리
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            # 무기 rect 정보 업데이트
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            # 충돌 체크
            if weapon_rect.colliderect(star_rect):
                weapon_to_remove = weapon_idx # 해당 무기 없애기 위한 값 설정
                star_to_remove = star_idx 

                # 가장 작은 크기의 장애물이 아니라면 다음 단계의 장애물로 나눠주기
                if star_img_idx < 3:
                    # 현재 장애물 크기 정보를 가지고 옴
                    star_width = star_rect.size[0]
                    star_height = star_rect.size[1]

                    # 나눠진 장애물 정보
                    small_star_rect = star_images[star_img_idx + 1].get_rect()
                    small_star_width = small_star_rect.size[0]
                    small_star_height = small_star_rect.size[1]

                    # 왼쪽으로 튕겨나가는 작은 장애물
                    stars.append({
                        "pos_x" : star_pos_x + (star_width / 2) - (small_star_width / 2), # 장애물의 x 좌표
                        "pos_y" : star_pos_y + (star_height / 2) - (small_star_height / 2), # 장애물의 y 좌표
                        "img_idx" : star_img_idx + 1, # 공의 이미지 인덱스
                        "to_x": -3, # x축 이동방향, -3 이면 왼쪽으로, 3 이면 오른쪽으로
                        "to_y": -6, # y축 이동방향,
                        "init_spd_y": star_speed_y[star_img_idx + 1]})# y 최초 속도

                    # 오른쪽으로 튕겨나가는 작은 장애물
                    stars.append({
                        "pos_x" : star_pos_x + (star_width / 2) - (small_star_width / 2), # 장애물의 x 좌표
                        "pos_y" : star_pos_y + (star_height / 2) - (small_star_height / 2), # 장애물의 y 좌표
                        "img_idx" : star_img_idx + 1, # 장애물의 이미지 인덱스
                        "to_x": 3, # x축 이동방향, -3 이면 왼쪽으로, 3 이면 오른쪽으로
                        "to_y": -6, # y축 이동방향,
                        "init_spd_y": star_speed_y[star_img_idx + 1]})# y 최초 속도

                break
        else: 
            continue 
        break 

    
    # 충돌된 장애물 or 무기 없애기
    if star_to_remove > -1:
        del stars[star_to_remove]
        star_to_remove = -1

    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1

    # 모든 장애물을 없앤 경우 게임 종료 (성공)
    if len(stars) == 0:
        game_result = "Mission Complete"
        running = False

    # 5. 화면에 그리기
    screen.blit(background, (0, 0))
    
    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    for idx, val in enumerate(stars):
        star_pos_x = val["pos_x"]
        star_pos_y = val["pos_y"]
        star_img_idx = val["img_idx"]
        screen.blit(star_images[star_img_idx], (star_pos_x, star_pos_y))

    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))
    
    # 경과 시간 계산
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 # ms -> s
    timer = game_font.render("Time : {}".format(int(total_time - elapsed_time)), True, (255, 255, 255))
    screen.blit(timer, (10, 10))

    # 시간 초과했다면
    if total_time - elapsed_time <= 0:
        game_result = "Time Over"
        running = False

    pygame.display.update()

# 게임 오버 메시지
msg = game_font.render(game_result, True, (255, 255, 0)) # 노란색
msg_rect = msg.get_rect(center=(int(screen_width / 2), int(screen_height / 2)))
screen.blit(msg, msg_rect)
pygame.display.update()

# 2초 대기
pygame.time.delay(2000)

pygame.quit()
