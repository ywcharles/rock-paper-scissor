import cv2 as cv
import mediapipe as mp
import random

def generateMove():
    gestures = ["paper", "rock", "scissor"]
    gesture_index = random.randint(0,2)
    return gestures[gesture_index]

def getHandMove(hand_landmarks):
    landmarks = hand_landmarks.landmark
    if all([landmarks[i].y < landmarks[i+3].y for i in range(9, 20, 4)]): return "rock"
    elif landmarks[13].y < landmarks[16].y and landmarks[17].y < landmarks[20].y: return "scissor"
    else: return "paper"

def detectWinner(computer, player):
    if computer == player: return "draw"
    
    if computer == "rock":
        if player == "scissor": return "lost"
        else: return "win"
    elif computer == "scissor":
        if player == "paper": return "lost"
        else: return "win"
    else:
        if player == "rock": return "lost"
        else: return "win"

if __name__=="__main__":
    # variables
    state = 0 # 0: before player move, 1: after player move, 2: after winner is displayed
    player_move = ""
    hands_on_screen = False
    computer_points = 0
    player_points = 0

    # media pipe set up
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_hands = mp.solutions.hands

    # image, font and cam set up
    bg = cv.imread('assets/rps_background.png', 1) # load bg
    bg = cv.resize(bg, (1200,800))
    cap = cv.VideoCapture(0) # init cam
    font = cv.FONT_HERSHEY_SIMPLEX

    # init hand detector
    with mp_hands.Hands(model_complexity=0,
                        min_detection_confidence=0.9,
                        min_tracking_confidence=0.9) as hands:
        
        #display cam loop
        while True:
            ret, frame = cap.read()

            # crop web cam image
            frame = frame[0:720, 280:1000]
            frame = cv.resize(frame, (400,400))

            # get hands from cam and display them
            frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB) # convert to rgb
            results = hands.process(frame)
            frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR) # convert back to gbr
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame,
                                                 hand_landmarks,
                                                 mp_hands.HAND_CONNECTIONS,
                                                 mp_drawing_styles.get_default_hand_landmarks_style(),
                                                 mp_drawing_styles.get_default_hand_connections_style())
            
            # get gesture and resize it
            if (state == 0):
                computer_move = generateMove()
                computer_move_img = cv.imread('assets/'+computer_move+'.png', 1)
                computer_move_img = cv.resize(computer_move_img, (400, 400))
            
            # get player hand gesture
            hls = results.multi_hand_landmarks
            if hls and (len(hls) > 0):
                if state == 0: # only get move if there's no move before
                    player_move = getHandMove(hls[0])
                    state = 1;
                hands_on_screen = True
            else:
                hands_on_screen = False
            
            frame = cv.flip(frame,1)

            # paste webcam
            img = bg.copy()
            img[270:670, 670:1070] = frame

            # put gesture in background after player move is detected
            if state == 1:
                img[270:670, 130:530] = computer_move_img

                # add move text
                img = cv.putText(img, computer_move, (260, 770), font, 1, (255,255,255),3, cv.LINE_AA)
                img = cv.putText(img, player_move, (830, 770), font, 1, (255,255,255),3, cv.LINE_AA)

                # get match result
                match_result = detectWinner(computer_move, player_move)

                # display result 
                img = cv.putText(img, match_result, (575, 400), font, 1, (0,0,255),3, cv.LINE_AA)

                # go to next round by going back to the 1st state of a round
                if not hands_on_screen: 
                    # increment points
                    if state == 1:
                        if match_result == "win": 
                            player_points += 1
                        elif match_result == "lost":
                            computer_points += 1
                    state = 0 

            else:
                img = cv.putText(img, "show your move on the screen" , (630, 770), font, 1, (0,0,255),3, cv.LINE_AA)

            # display score
            img = cv.putText(img, str(player_points), (1075, 250), font, 1, (0,0,255),3, cv.LINE_AA)
            img = cv.putText(img, str(computer_points), (100, 250), font, 1, (0,0,255),3, cv.LINE_AA)

            # add webcam to background 
            cv.imshow('frame', img)

            # end window
            if cv.waitKey(1) == ord('q'):
                break


    cap.release()
    cv.destroyAllWindows()