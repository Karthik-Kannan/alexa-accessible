import os, sys, inspect, thread, time

src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = os.path.abspath(os.path.join(src_dir, '../lib'))
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap
import urllib2
import json
import os
import threading

actions = ['clockwise', 'counterclockwise', 'vertical swipe', 'horizontal swipe', 'tap']

# def get_alexa_map():
#   print time.time()
#   response = urllib2.urlopen('http://656305d5.ngrok.io/get_json/')
#   data = json.load(response)
#   alexa_map = {}
#   for action in actions:
#     if action in data.keys():
#       alexa_map[action] = data[action]
#     else:
#       alexa_map[action] = None
#   with open("alexa_actions.json" , 'w') as f:
#     f.write(json.dumps(alexa_map))

# def start_thread():
#   threading.Timer(3.0, get_alexa_map).start()

wakeword = 'Alexa,'  

class LeapListener(Leap.Listener):

  def on_init(self, controller):
    # start_thread()
    with open("alexa_actions.json", 'r') as f:
      self.alexa_map = json.load(f)

  def on_connect(self, controller):
    print "Connected"

  def on_frame (self, controller):
    try:
      with open("alexa_actions.json", 'r') as f:
        self.alexa_map = json.load(f)
    except:
      pass

    frame   = controller.frame()
    
    right_hand = frame.hands[0] if frame.hands[0].is_right else frame.hands[1]
    pointed_fingers = sum([1 if pointable.is_extended else 0 for pointable in right_hand.pointables])

    gesture = frame.gestures()[0]
    if gesture.type is Leap.Gesture.TYPE_SWIPE:
      swipe = Leap.SwipeGesture(gesture)
      if swipe.direction[0] > 0.5 and pointed_fingers > 3 and self.alexa_map['horizontal swipe'] is not None:
        os.system("say " + wakeword + self.alexa_map['horizontal swipe'])
      elif swipe.direction[1] > 0.5 and pointed_fingers > 3 and self.alexa_map['vertical swipe'] is not None:
        os.system("say " + wakeword + self.alexa_map['vertical swipe'])

    
    elif gesture.type is Leap.Gesture.TYPE_CIRCLE:
      circle = Leap.CircleGesture(gesture)
      if (circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2) and pointed_fingers == 1 and self.alexa_map['clockwise'] is not None:
        os.system("say " + wakeword + self.alexa_map['clockwise'])
      elif (circle.pointable.direction.angle_to(circle.normal) > Leap.PI/2) and pointed_fingers == 1 and self.alexa_map['counterclockwise'] is not None:
        os.system("say " + wakeword + self.alexa_map['counterclockwise'])
     
    else:
      if len(frame.hands) > 1 and self.alexa_map['tap'] is not None:
        os.system("say " + wakeword + self.alexa_map['tap'])


    # all_hands = frame.hands
    # right_hand = frame.hands.rightmost
    # right_pointable = right_hand.pointables
    # count = 0
    # for pointable in right_pointable:
    #   if not pointable.is_extended:
    #      count += 1

    # for gesture in frame.gestures():
    #   if gesture.type is Leap.Gesture.TYPE_SWIPE:
    #     print "count", count
    #     if count == 0:
    #       swipe = Leap.SwipeGesture(gesture)

    #       x_mov = swipe.direction[0]
    #       y_mov = swipe.direction[1]
          
    #       if abs(x_mov) > 0.3:
    #         if x_mov > 0:
    #           os.system("say 'Alexa, stop music'")
    #       elif abs(y_mov) > 0.3:
    #         if y_mov > 0:
    #           os.system("say 'Alexa, play music'")

    #   elif gesture.type is Leap.Gesture.TYPE_CIRCLE:
    #     if count > 3:
    #       circle = Leap.CircleGesture(gesture)
    #       if (circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2):
    #         dir = "clockwise"
    #         os.system("say 'Alexa, increase volume'")
    #       else:
    #         dir = "counterclockwise"
    #         os.system("say 'Alexa, lower volume'")    

    # if count == 2 and len(frame.hands) == 2:
    #   os.system("say 'Alexa, tell me the time'")
    # print len(all_hands)

     
      # elif gesture.type is Leap.Gesture.TYPE_SWIPE:
      #   swipe = Leap.SwipeGesture(gesture)

      #   x_mov = swipe.direction[0]
      #   y_mov = swipe.direction[1]
        
      #   if abs(x_mov) > 0.3:
      #     if x_mov < 0:
      #       print "left swipe"
      #     else:
      #       print "right swipe"
      #   elif abs(y_mov) > 0.3:
      #     if y_mov < 0:
      #       print "down"
      #       # os.system("say 'Alexa, lower volume'")
      #     else:
      #       print "iup"
      #       # os.system("say 'Alexa, increase volume'") 

      # else:
      #   extended_finger_list = frame.fingers.extended()
      #   if len(extended_finger_list) == 5:
      #      print "open fist"
      #   else:
      #      print "closed fist"


def main():
  listener   = LeapListener()
  controller = Leap.Controller()

  controller.add_listener(listener)

  controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)
  controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)
  controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP)
  controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP)
  
  controller.config.set("Gesture.Circle.MinRadius", 10.0)
  controller.config.set("Gesture.Circle.MinArc", .5)

  controller.config.set("Gesture.Swipe.MinLength", 20.0)
  controller.config.set("Gesture.Swipe.MinVelocity", 350)

  controller.config.save()

  print "Press Enter to quit..."
  
  try:
     sys.stdin.readline()
  except KeyboardInterrupt:
     pass
  finally:
     controller.remove_listener(listener)

if __name__ == "__main__":
  main()
