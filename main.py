from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader
from kivy.base import stopTouchApp
from kivy.clock import mainthread
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line, Ellipse
from kivy.utils import get_color_from_hex
from functools import partial
import random
import math
from kivy.uix.scatter import Scatter

# Constants
ENEMY_SPEED = 0.3
CORRECT_COLOR = (0, 1, 0, 1)  # Green color for correct words
WRONG_COLOR = (1, 0, 0, 1)    # Red color for wrong words
SPEED_LEVELS = {
    0: 0.3,     
    100: 0.4,   
    200: 0.5,   
    300: 0.6,   
    400: 0.7,   
    500: 0.8,   
    600: 0.9,   
    700: 1.0    
}

class TypingAttackGame(BoxLayout):
    def __init__(self, screen_manager=None, **kwargs):
        super(TypingAttackGame, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.screen_manager = screen_manager
        self.paused = False
        
        # เพิ่มตัวแปรสำหรับระบบใหม่
        self.combo_count = 0
        self.max_combo = 0
        self.power_ups = []
        self.particles = []
        self.backgrounds = []
        self.active_effects = {
            'double_score': False,
            'slow_motion': False,
            'clear_screen': False
        }
        self.effect_timers = {
            'double_score': 0,
            'slow_motion': 0
        }
        
        # Initialize variables
        self.score = 0
        self.enemies = []
        self.remaining_time = 180
        self.current_speed = SPEED_LEVELS[0]
        
        # Load sound effects
        self.correct_sound = SoundLoader.load("D:\\Y1\\StudyY1\\TypingSurvival\\sound\\hit.mp3")
        self.incorrect_sound = SoundLoader.load("D:\\Y1\\StudyY1\\TypingSurvival\\sound\\sound_miss.mp3")
        self.sound = SoundLoader.load("D:\\Y1\\StudyY1\\TypingSurvival\\sound\\sound_sound6.mp3")
        
        if self.sound:
            self.sound.volume = 0.03
            self.sound.play()

        # Create control buttons layout
        control_layout = BoxLayout(size_hint=(1, 0.1), spacing=5)
        pause_button = Button(text="Pause", font_size=24)
        pause_button.bind(on_press=self.show_pause_popup)
        
        restart_button = Button(text="Restart", font_size=24)
        restart_button.bind(on_press=self.restart_game)
        
        home_button = Button(text="Home", font_size=24)
        home_button.bind(on_press=self.go_home)
        
        exit_button = Button(text="Exit", font_size=24)
        exit_button.bind(on_press=self.exit_game)
        
        control_layout.add_widget(pause_button)
        control_layout.add_widget(restart_button)
        control_layout.add_widget(home_button)
        control_layout.add_widget(exit_button)
        
        self.add_widget(control_layout)

        # Create info layout for score and timer
        info_layout = BoxLayout(size_hint=(1, 0.1))
        self.score_label = Label(text=f"Score: {self.score}", font_size=36)
        self.timer_label = Label(text=f"Time: {self.remaining_time}", font_size=30)
        self.high_score_label = Label(text=f"High Score: {self.get_high_score()}", font_size=30)
        self.speed_notification = Label(
            text="",
            font_size=30,
            color=(1, 1, 0, 1)
        )
        
        info_layout.add_widget(self.score_label)
        info_layout.add_widget(self.timer_label)
        info_layout.add_widget(self.high_score_label)
        info_layout.add_widget(self.speed_notification)
        self.add_widget(info_layout)

        # เพิ่ม UI สำหรับ Combo และ Active Effects
        status_layout = BoxLayout(size_hint=(1, 0.1))
        self.combo_label = Label(
            text="Combo: 0",
            font_size=24,
            color=(1, 0.8, 0, 1)  # สีเหลืองทอง
        )
        self.effects_label = Label(
            text="",
            font_size=24,
            color=(0, 1, 1, 1)  # สีฟ้า
        )
        status_layout.add_widget(self.combo_label)
        status_layout.add_widget(self.effects_label)
        self.add_widget(status_layout)
        
        # Game area
        self.game_area = Widget(size_hint=(1, 0.6))
        self.add_widget(self.game_area)

        # Text input
        self.text_input = TextInput(
            multiline=False,
            size_hint=(1, 0.1),
            font_size=30,
            background_color=(1, 1, 1, 1)
        )
        self.text_input.bind(on_text_validate=self.on_text_validate)
        self.add_widget(self.text_input)

        # Load words and start game
        self.word_list = self.load_words_from_file("D:\\Y1\\StudyY1\\TypingSurvival\\words.txt")
        self.create_animated_background()
        Clock.schedule_interval(self.update_background, 1/30)
        Clock.schedule_interval(self.spawn_enemy, 2)
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        Clock.schedule_interval(self.update_timer, 1.0)
        Clock.schedule_interval(self.spawn_power_up, 15)  # spawn power-up ทุก 15 วินาที
    def create_animated_background(self):
        """สร้าง background เคลื่อนไหวด้วยรูปทรงเรขาคณิต"""
        for i in range(10):  # จำนวนรูปทรงพื้นหลัง
            size = random.randint(20, 50)
            bg_shape = {
                'widget': Widget(size=(size, size)),
                'speed': random.uniform(0.5, 2),
                'angle': random.uniform(0, 360)
            }
            
            with bg_shape['widget'].canvas:
                Color(*get_color_from_hex('#1a1a1a'))
                RoundedRectangle(pos=bg_shape['widget'].pos, 
                               size=bg_shape['widget'].size,
                               radius=[size/4])
            
            bg_shape['widget'].pos = (
                random.randint(0, Window.width),
                random.randint(0, Window.height)
            )
            self.backgrounds.append(bg_shape)
            self.game_area.add_widget(bg_shape['widget'])

    def update_background(self, dt):
        """อัพเดทการเคลื่อนที่ของ background"""
        if self.paused:
            return
            
        for bg in self.backgrounds:
            # เคลื่อนที่แบบ sine wave
            bg['angle'] += bg['speed'] * dt
            bg['widget'].x += math.sin(bg['angle']) * 2
            bg['widget'].y -= bg['speed']
            
            # วนกลับเมื่อออกจากหน้าจอ
            if bg['widget'].y < -bg['widget'].height:
                bg['widget'].y = Window.height + bg['widget'].height
                bg['widget'].x = random.randint(0, Window.width)

    def create_word_destroy_effect(self, pos, word_color):
        """สร้าง particle effect เมื่อทำลายคำ"""
        num_particles = 20
        for i in range(num_particles):
            particle = Label(
                text="✦",  # หรือใช้ "•", "*", "×" 
                font_size=random.randint(10, 20),
                pos=pos,
                color=word_color
            )
            
            # สุ่มทิศทางการกระจาย
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(50, 150)
            dx = math.cos(angle) * distance
            dy = math.sin(angle) * distance
            
            # สร้าง animation
            anim = Animation(
                pos=(pos[0] + dx, pos[1] + dy),
                opacity=0,
                duration=random.uniform(0.5, 1.0)
            )
            
            self.game_area.add_widget(particle)
            self.particles.append(particle)
            
            # ลบ particle เมื่อ animation จบ
            anim.bind(on_complete=lambda *args: self.remove_particle(particle))
            anim.start(particle)

    def remove_particle(self, particle):
        """ลบ particle ออกจากหน้าจอ"""
        if particle in self.particles:
            self.game_area.remove_widget(particle)
            self.particles.remove(particle)

    def spawn_enemy(self, dt):
        if self.paused:
            return
            
        if self.word_list and len(self.enemies) < 12:
            enemy_word = random.choice(self.word_list)
            enemy = Label(
                text=enemy_word,
                font_size=random.randint(45, 50)
            )
            
            # เพิ่ม animation การปรากฏตัว
            enemy.opacity = 0
            spawn_anim = Animation(opacity=1, duration=0.3)
            spawn_anim.start(enemy)
            
            # สุ่มสีของคำ
            hue = random.random()
            enemy.color = self.hsv_to_rgb(hue, 0.7, 1)
            
            word_width = len(enemy_word) * (enemy.font_size * 0.6)
            max_x = Window.width - word_width
            enemy.x = random.randint(0, int(max_x))
            enemy.y = Window.height
            
            self.enemies.append(enemy)
            self.game_area.add_widget(enemy)

    def hsv_to_rgb(self, h, s, v):
        """แปลงสี HSV เป็น RGB"""
        if s == 0.0:
            return (v, v, v)
            
        i = int(h * 6.0)
        f = (h * 6.0) - i
        p = v * (1.0 - s)
        q = v * (1.0 - s * f)
        t = v * (1.0 - s * (1.0 - f))
        i = i % 6
        
        if i == 0:
            return (v, t, p)
        if i == 1:
            return (q, v, p)
        if i == 2:
            return (p, v, t)
        if i == 3:
            return (p, q, v)
        if i == 4:
            return (t, p, v)
        if i == 5:
            return (v, p, q)
        
    def spawn_power_up(self, dt):
        if self.paused or len(self.power_ups) >= 3:
            return
            
        power_up_types = [
            {'type': 'time', 'text': 'Time', 'color': (0, 1, 0, 1)},
            {'type': 'double_score', 'text': '2x', 'color': (1, 1, 0, 1)},
            {'type': 'slow_motion', 'text': 'SLOW', 'color': (0, 1, 1, 1)},
            {'type': 'clear_screen', 'text': 'CLEAR', 'color': (1, 0, 1, 1)}
        ]
        
        power_up_info = random.choice(power_up_types)
        power_up = Label(
            text=power_up_info['text'],
            font_size=40,
            color=power_up_info['color'],
            size_hint=(None, None),
            size=(60, 60)
        )
        power_up.power_up_type = power_up_info['type']
        
        power_up.x = random.randint(0, Window.width - 60)
        power_up.y = Window.height
        
        self.power_ups.append(power_up)
        self.game_area.add_widget(power_up)

    def go_home(self, instance):
        self.score = 0
        self.remaining_time = 180
        self.enemies.clear()
        self.game_area.clear_widgets()
        Clock.unschedule(self.update_timer)
        Clock.unschedule(self.update)
        Clock.unschedule(self.spawn_enemy)
        Clock.unschedule(self.spawn_power_up)
        self.screen_manager.current = 'start'

    def exit_game(self, instance):
        Window.fullscreen = False
        stopTouchApp()

    def update_speed(self):
        new_speed = SPEED_LEVELS[0]
        current_level = 0
        
        for score_threshold, speed in SPEED_LEVELS.items():
            if self.score >= score_threshold:
                new_speed = speed
                current_level = score_threshold
            else:
                break
        
        if new_speed != self.current_speed:
            self.current_speed = new_speed
            self.show_speed_notification(current_level)

    def show_speed_notification(self, level):
        self.speed_notification.text = f"Speed Level {level//100 + 1}!"
        Clock.schedule_once(self.clear_speed_notification, 2)

    def clear_speed_notification(self, dt):
        self.speed_notification.text = ""
        
    def load_words_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                words = [line.strip() for line in file.readlines() if line.strip()]
                return words
        except FileNotFoundError:
            print(f"Error: {filename} not found.")
            return []

    def reset_text_input_color(self, dt):
        self.text_input.background_color = (1, 1, 1, 1)

    def reset_score_label_color(self, dt):
        self.score_label.color = (1, 1, 1, 1)

    @mainthread
    def set_focus(self, dt):
        if self.text_input:
            self.text_input.focus = True

    # ลบฟังก์ชัน _on_keyboard_down ออก เพราะไม่จำเป็นต้องใช้

    def show_pause_popup(self, instance):
        self.paused = True
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text="Game Paused", font_size=30))
        
        resume_button = Button(text="Resume", font_size=24, size_hint=(1, 0.3))
        resume_button.bind(on_press=self.dismiss_pause_popup)
        content.add_widget(resume_button)
        
        self.pause_popup = Popup(
            title="Pause",
            content=content,
            size_hint=(None, None),
            size=(400, 200),
            auto_dismiss=False
        )
        self.pause_popup.open()

    def dismiss_pause_popup(self, instance):
        self.paused = False
        self.pause_popup.dismiss()
        Clock.schedule_once(lambda dt: setattr(self.text_input, 'focus', True), 0.1)

    def update(self, dt):
        if self.paused:
            return
            
        # อัพเดทการเคลื่อนที่ของ enemies
        current_speed = self.current_speed
        if self.active_effects['slow_motion']:
            current_speed *= 0.5
            
        for enemy in list(self.enemies):
            enemy.y -= current_speed
            if enemy.y < 0:
                self.handle_missed_word(enemy)
                
        # อัพเดทการเคลื่อนที่ของ power-ups
        for power_up in list(self.power_ups):
            power_up.y -= 2
            if power_up.y < 0:
                self.game_area.remove_widget(power_up)
                self.power_ups.remove(power_up)
                
        # อัพเดท effect timers
        for effect, timer in list(self.effect_timers.items()):
            if timer > 0:
                self.effect_timers[effect] -= dt
                if self.effect_timers[effect] <= 0:
                    self.active_effects[effect] = False
                    self.effect_timers[effect] = 0
                    
        # อัพเดทแสดงผล active effects
        active_effects_text = []
        if self.active_effects['double_score']:
            active_effects_text.append("2x SCORE")
        if self.active_effects['slow_motion']:
            active_effects_text.append("SLOW MO")
        self.effects_label.text = " | ".join(active_effects_text)

    def update_timer(self, dt):
        if self.paused:
            return
            
        self.remaining_time -= 1
        self.timer_label.text = f"Time: {max(0, self.remaining_time)}"
        
        if self.remaining_time <= 0:
            self.end_game()

    def collect_power_up(self, power_up):
        if power_up.power_up_type == 'time':
            self.remaining_time += 30
            self.show_floating_text("+30s", power_up.x, power_up.y)
        elif power_up.power_up_type == 'double_score':
            self.active_effects['double_score'] = True
            self.effect_timers['double_score'] = 10  # 10 วินาที
            self.show_floating_text("2x SCORE", power_up.x, power_up.y)
        elif power_up.power_up_type == 'slow_motion':
            self.active_effects['slow_motion'] = True
            self.effect_timers['slow_motion'] = 5  # 5 วินาที
            self.show_floating_text("SLOW MOTION", power_up.x, power_up.y)
        elif power_up.power_up_type == 'clear_screen':
            for enemy in list(self.enemies):
                self.game_area.remove_widget(enemy)
            self.enemies.clear()
            self.show_floating_text("CLEAR!", Window.width/2, Window.height/2)
            
        self.game_area.remove_widget(power_up)
        self.power_ups.remove(power_up)
        Clock.schedule_once(self.set_focus, 0.1)
    def handle_missed_word(self, enemy):
        try:
            self.game_area.remove_widget(enemy)
            self.enemies.remove(enemy)
            
            self.score = max(0, self.score - 5)
            self.score_label.text = f"Score: {self.score}"
            
            self.combo_count = 0  # Reset combo when missing a word
            self.combo_label.text = "Combo: 0"
            
            self.score_label.color = (1, 0, 0, 1)
            Clock.schedule_once(self.reset_score_label_color, 0.3)
            
            if len(self.enemies) < 6:  # ปรับจาก 10 เป็น 6 (ครึ่งหนึ่งของค่าสูงสุด)
                Clock.unschedule(self.spawn_enemy)
                Clock.schedule_interval(self.spawn_enemy, 1)
            else:
                Clock.unschedule(self.spawn_enemy)
                Clock.schedule_interval(self.spawn_enemy, 2)
                
        except:
            pass

    def show_time_penalty_notification(self):
        """Show a temporary notification when time penalty is applied"""
        # Change timer label color to red
        self.timer_label.color = (1, 0, 0, 1)
        
        # Create and position the penalty label
        penalty_label = Label(
            text="-20 seconds!",
            font_size=30,
            color=(1, 0, 0, 1),
            opacity=1.0,
            pos=(Window.width / 2 - 50, Window.height / 2)  # Center the label
        )
        self.game_area.add_widget(penalty_label)
        
        # Create fade out and move up animation
        anim = Animation(
            opacity=0,
            pos=(penalty_label.x, penalty_label.y + 100),
            duration=1.0
        )
        
        # Remove the label when animation completes
        def on_complete(*args):
            self.game_area.remove_widget(penalty_label)
        anim.bind(on_complete=on_complete)
        
        # Start the animation
        anim.start(penalty_label)
        
        # Reset timer label color after delay
        Clock.schedule_once(lambda dt: setattr(self.timer_label, 'color', (1, 1, 1, 1)), 0.5)
        class AnimationState:
            def __init__(self, label):
                self.label = label
                self.opacity = 1.0
        
        state = AnimationState(penalty_label)    
        # ทำให้ข้อความค่อยๆ เลื่อนขึ้นและจางหายไป
        def animate_penalty(dt):
            
            Clock.schedule_interval(animate_penalty, 1/30)
            
            # คืนสีของ timer_label กลับเป็นปกติ
        def reset_timer_color(dt):
            self.timer_label.color = (1, 1, 1, 1)  # สีขาว
            
            Clock.schedule_once(reset_timer_color, 0.5)
        
    def on_text_validate(self, instance):
        if self.paused:
            return
            
        typed_word = instance.text.strip()
        if not typed_word:
            return
            
        word_matched = False
        
        # Check for power-up collisions
        for power_up in list(self.power_ups):
            if typed_word.lower() == power_up.text.lower():
                self.collect_power_up(power_up)
                instance.text = ""
                Clock.schedule_once(lambda dt: setattr(self.text_input, 'focus', True), 0.1)
                return
        
        # Check regular words
        for enemy in list(self.enemies):
            if typed_word.lower() == enemy.text.lower():
                # Play correct sound
                if self.correct_sound:
                    self.correct_sound.play()
                    
                # Calculate score with combo
                base_score = 10
                combo_multiplier = min(2, 1 + (self.combo_count * 0.1))
                score_gain = int(base_score * combo_multiplier)
                
                if self.active_effects['double_score']:
                    score_gain *= 2
                    
                self.score += score_gain
                self.score_label.text = f"Score: {self.score}"
                
                # Update combo
                self.combo_count += 1
                self.max_combo = max(self.max_combo, self.combo_count)
                self.combo_label.text = f"Combo: {self.combo_count}"
                
                # Show floating score and animate enemy destruction
                self.show_floating_text(f"+{score_gain}", enemy.x, enemy.y)
                
                if self.combo_count > 0 and self.combo_count % 5 == 0:
                    self.show_floating_text(f"COMBO x{self.combo_count}!", 
                                            Window.width/2, Window.height/2)
                
                # Animate enemy destruction
                destroy_anim = Animation(opacity=0, duration=0.2)
                destroy_anim.bind(on_complete=lambda anim, widget: self.remove_enemy(enemy))
                destroy_anim.start(enemy)
                
                word_matched = True
                break
                
        if not word_matched:
            # Play incorrect sound
            if self.incorrect_sound:
                self.incorrect_sound.play()
                
            self.combo_count = 0
            self.combo_label.text = "Combo: 0"
            
            # Time penalty
            self.remaining_time = max(0, self.remaining_time - 20)
            self.timer_label.text = f"Time: {self.remaining_time}"
            
            # Show time penalty notification
            self.show_time_penalty_notification()
            
            if self.remaining_time <= 0:
                final_high_score = self.get_high_score()
                if self.score > final_high_score:
                    self.set_high_score(self.score)
                self.end_game()
            
        instance.text = ""
        self.text_input.background_color = CORRECT_COLOR if word_matched else WRONG_COLOR
        Clock.schedule_once(self.reset_text_input_color, 0.3)
        Clock.schedule_once(lambda dt: setattr(self.text_input, 'focus', True), 0.1)

    def remove_enemy(self, enemy):
        """Safely remove an enemy from the game area and enemies list"""
        try:
            self.game_area.remove_widget(enemy)
            self.enemies.remove(enemy)
        except:
            pass

    def show_floating_text(self, text, x, y):
        """Show floating text with fade out and upward movement animation"""
        label = Label(
            text=text,
            font_size=30,
            color=(1, 1, 1, 1),
            pos=(x, y)
        )
        self.game_area.add_widget(label)
        
        # Create animation that moves up and fades out
        float_anim = Animation(
            y=y + 100,  # Move up by 100 pixels
            opacity=0,   # Fade to transparent
            duration=1   # Over 1 second
        )
        float_anim.bind(on_complete=lambda anim, widget: self.game_area.remove_widget(widget))
        float_anim.start(label)
        # ทำให้ข้อความค่อยๆ เลื่อนขึ้นและจางหายไป
        def animate_penalty(dt):
        
            Clock.schedule_interval(animate_penalty, 1/30)
            
            # คืนสีของ timer_label กลับเป็นปกติ
            def reset_timer_color(dt):
                self.timer_label.color = (1, 1, 1, 1)  # สีขาว
            
            Clock.schedule_once(reset_timer_color, 0.5)

    def end_game(self):
        Clock.unschedule(self.update_timer)
        Clock.unschedule(self.update)
        Clock.unschedule(self.spawn_enemy)
        Clock.unschedule(self.spawn_power_up)
        
        current_high_score = self.get_high_score()
        if self.score > current_high_score:
            self.set_high_score(self.score)
            
        game_over_screen = self.screen_manager.get_screen('game_over')
        game_over_screen.score = self.score
        game_over_screen.max_combo = self.max_combo
        game_over_screen.update_score_label()
        self.screen_manager.current = 'game_over'

    def restart_game(self, instance):
        self.score = 0
        self.score_label.text = f"Score: {self.score}"
        self.remaining_time = 180
        self.timer_label.text = f"Time: {self.remaining_time}"
        self.timer_label.color = (1, 1, 1, 1)
        
        # Reset combo system
        self.combo_count = 0
        self.max_combo = 0
        self.combo_label.text = "Combo: 0"
        
        # Reset effects
        self.active_effects = {
            'double_score': False,
            'slow_motion': False,
            'clear_screen': False
        }
        self.effect_timers = {
            'double_score': 0,
            'slow_motion': 0
        }
        self.effects_label.text = ""
        
        # Clear enemies and power-ups
        for enemy in list(self.enemies):
            try:
                self.game_area.remove_widget(enemy)
            except:
                pass
        self.enemies.clear()
        
        for power_up in list(self.power_ups):
            try:
                self.game_area.remove_widget(power_up)
            except:
                pass
        self.power_ups.clear()
        
        # Reset game state
        self.current_speed = SPEED_LEVELS[0]
        self.text_input.text = ""
        self.paused = False
        
        # Restart timers
        Clock.unschedule(self.update_timer)
        Clock.unschedule(self.update)
        Clock.unschedule(self.spawn_enemy)
        Clock.unschedule(self.spawn_power_up)
        Clock.schedule_interval(self.update_timer, 1.0)
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        Clock.schedule_interval(self.spawn_enemy, 2)
        Clock.schedule_interval(self.spawn_power_up, 15)
        Clock.schedule_once(lambda dt: setattr(self.text_input, 'focus', True), 0.1)

    def get_high_score(self):
        try:
            with open("D:\\Y1\\StudyY1\\TypingSurvival\\high_score.txt", "r") as file:
                return int(file.read())
        except FileNotFoundError:
            return 0
        except:
            return 0

    def set_high_score(self, score):
        try:
            with open("D:\\Y1\\StudyY1\\TypingSurvival\\high_score.txt", "w") as file:
                file.write(str(score))
            self.high_score_label.text = f"High Score: {score}"
        except Exception as e:
            print(f"Error saving high score: {e}")

class GameOverScreen(Screen):
    def __init__(self, screen_manager, **kwargs):
        super(GameOverScreen, self).__init__(**kwargs)
        self.screen_manager = screen_manager
        self.score = 0
        self.max_combo = 0

        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        
        game_over_label = Label(
            text="Game Over",
            font_size=48,
            size_hint=(1, 0.3)
        )
        
        # เพิ่ม layout สำหรับแสดงคะแนนและ combo
        stats_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.4))
        
        self.score_label = Label(
            text=f"Your Score: {self.score}",
            font_size=36,
            size_hint=(1, 0.5)
        )
        
        self.combo_label = Label(
            text=f"Max Combo: {self.max_combo}",
            font_size=30,
            size_hint=(1, 0.5),
            color=(1, 0.8, 0, 1)  # สีเหลืองทอง
        )
        
        stats_layout.add_widget(self.score_label)
        stats_layout.add_widget(self.combo_label)
        
        button_layout = BoxLayout(
            orientation='horizontal', 
            spacing=10,
            size_hint=(1, 0.2)
        )
        
        restart_button = Button(
            text="New Game",
            font_size=24,
            size_hint=(0.5, 1)
        )
        restart_button.bind(on_press=self.restart_game)
        
        home_button = Button(
            text="Home",
            font_size=24,
            size_hint=(0.5, 1)
        )
        home_button.bind(on_press=self.go_home)
        
        button_layout.add_widget(restart_button)
        button_layout.add_widget(home_button)
        
        layout.add_widget(game_over_label)
        layout.add_widget(stats_layout)
        layout.add_widget(button_layout)
        
        self.add_widget(layout)

    def go_home(self, instance):
        self.screen_manager.current = 'start'

    def restart_game(self, instance):
        game_screen = self.screen_manager.get_screen('game')
        game_screen.children[0].restart_game(None)
        self.screen_manager.current = 'game'

    def update_score_label(self):
        self.score_label.text = f"Your Score: {self.score}"
        self.combo_label.text = f"Max Combo: {self.max_combo}"

class BorderedLabel(BoxLayout):
    def __init__(self, text='', font_size=24, **kwargs):
        super(BorderedLabel, self).__init__(**kwargs)

        with self.canvas.before:
            Color(0.5, 0.5, 0.5, 1)
            self.border = Rectangle(pos=self.pos, size=self.size)

        self.label = Label(
            text=text,
            font_size=font_size,
            size_hint=(1, 1),
            color=(9, 0, 9, 9)
        )
        self.add_widget(self.label)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.border.pos = self.pos
        self.border.size = self.size

class StartScreen(Screen):
    def __init__(self, screen_manager, **kwargs):
        super(StartScreen, self).__init__(**kwargs)
        self.screen_manager = screen_manager

        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        
        title_label = BorderedLabel(
            text="TYPING-ATTACK",
            font_size=70,
            size_hint=(1, 0.4)
        )
        
        start_button = Button(
            text="Start Game",
            font_size=36,
            size_hint=(1, 0.2),
            color=(0, 0, 9, 1)
        )
        start_button.bind(on_press=self.start_game)
        
        high_score_button = Button(
            text="High Score",
            font_size=24,
            size_hint=(1, 0.1),
            color=(0, 6, 6, 1)
        )
        high_score_button.bind(on_press=self.view_high_score)
        
        volume_layout = BoxLayout(size_hint=(1, 0.1), spacing=5)
        
        volume_up_button = Button(
            text="Volume Up",
            font_size=24,
            color=(6, 0, 0, 1)
        )
        volume_up_button.bind(on_press=self.volume_up)
        volume_down_button = Button(
            text="Volume Down",
            font_size=24,
            color=(0, 1, 0, 1)
        )
        volume_down_button.bind(on_press=self.volume_down)
        
        volume_layout.add_widget(volume_up_button)
        volume_layout.add_widget(volume_down_button)
        
        layout.add_widget(title_label)
        layout.add_widget(start_button)
        layout.add_widget(high_score_button)
        layout.add_widget(volume_layout)
        
        self.add_widget(layout)

    def view_high_score(self, instance):
        self.screen_manager.current = 'high_score'

    def volume_up(self, instance):
        game_screen = self.screen_manager.get_screen('game').children[0]
        if hasattr(game_screen, 'sound') and game_screen.sound:
            game_screen.sound.volume = min(1, game_screen.sound.volume + 0.1)

    def volume_down(self, instance):
        game_screen = self.screen_manager.get_screen('game').children[0]
        if hasattr(game_screen, 'sound') and game_screen.sound:
            game_screen.sound.volume = max(0, game_screen.sound.volume - 0.1)

    def start_game(self, instance):
        self.screen_manager.current = 'game'
        
    def on_text_validate(self, instance):
        if self.paused:
            return
            
        typed_word = instance.text.strip()
        if not typed_word:
            return
            
        word_matched = False
        
        # ตรวจสอบการชน power-up
        for power_up in list(self.power_ups):
            if typed_word.lower() == power_up.text.lower():
                self.collect_power_up(power_up)
                instance.text = ""
                return
        
        # ตรวจสอบคำปกติ
        for enemy in list(self.enemies):
            if typed_word.lower() == enemy.text.lower():
                # คำนวณคะแนนพร้อม combo
                base_score = 10
                combo_multiplier = min(2, 1 + (self.combo_count * 0.1))
                score_gain = int(base_score * combo_multiplier)
                
                if self.active_effects['double_score']:
                    score_gain *= 2
                    
                self.score += score_gain
                self.score_label.text = f"Score: {self.score}"
                
                # อัพเดท combo
                self.combo_count += 1
                self.max_combo = max(self.max_combo, self.combo_count)
                self.combo_label.text = f"Combo: {self.combo_count}"
                
                # แสดง floating score
                self.show_floating_text(f"+{score_gain}", enemy.x, enemy.y)
                
                if self.combo_count > 0 and self.combo_count % 5 == 0:
                    self.show_floating_text(f"COMBO x{self.combo_count}!", 
                                            Window.width/2, Window.height/2)
                
                try:
                    self.game_area.remove_widget(enemy)
                    self.enemies.remove(enemy)
                except:
                    pass
                    
                word_matched = True
                break
                
        if not word_matched:
            self.combo_count = 0
            self.combo_label.text = "Combo: 0"
            
            # ถ้าพิมพ์ผิด
            self.remaining_time = max(0, self.remaining_time - 20)
            self.timer_label.text = f"Time: {self.remaining_time}"
            
            # แสดงการแจ้งเตือนลดเวลา
            self.show_time_penalty_notification()
            
            if self.remaining_time <= 0:
                final_high_score = self.get_high_score()
                if self.score > final_high_score:
                    self.set_high_score(self.score)
                self.end_game()
            
        instance.text = ""
        self.text_input.background_color = CORRECT_COLOR if word_matched else WRONG_COLOR
        Clock.schedule_once(self.reset_text_input_color, 0.3)
        Clock.schedule_once(self.set_focus, 0.1)

    def show_floating_text(self, text, x, y):
        """แสดงข้อความลอยที่จะค่อยๆ เลื่อนขึ้นและจางหาย"""
        label = Label(
            text=text,
            font_size=30,
            color=(1, 1, 1, 1),
            pos=(x, y)
        )
        self.game_area.add_widget(label)
        
        anim = Animation(y=y+100, opacity=0, duration=1)
        anim.bind(on_complete=lambda *args: self.game_area.remove_widget(label))
        anim.start(label)

    def end_game(self):
        Clock.unschedule(self.update_timer)
        Clock.unschedule(self.update)
        Clock.unschedule(self.spawn_enemy)
        Clock.unschedule(self.spawn_power_up)
        
        current_high_score = self.get_high_score()
        if self.score > current_high_score:
            self.set_high_score(self.score)
            
        game_over_screen = self.screen_manager.get_screen('game_over')
        game_over_screen.score = self.score
        game_over_screen.max_combo = self.max_combo
        game_over_screen.update_score_label()
        self.screen_manager.current = 'game_over'

    def restart_game(self, instance):
        self.score = 0
        self.score_label.text = f"Score: {self.score}"
        self.remaining_time = 180
        self.timer_label.text = f"Time: {self.remaining_time}"
        self.timer_label.color = (1, 1, 1, 1)
        
        # Reset combo system
        self.combo_count = 0
        self.max_combo = 0
        self.combo_label.text = "Combo: 0"
        
        # Reset effects
        self.active_effects = {
            'double_score': False,
            'slow_motion': False,
            'clear_screen': False
        }
        self.effect_timers = {
            'double_score': 0,
            'slow_motion': 0
        }
        self.effects_label.text = ""
        
        # Clear enemies and power-ups
        for enemy in list(self.enemies):
            try:
                self.game_area.remove_widget(enemy)
            except:
                pass
        self.enemies.clear()
        
        for power_up in list(self.power_ups):
            try:
                self.game_area.remove_widget(power_up)
            except:
                pass
        self.power_ups.clear()
        
        # Reset game state
        self.current_speed = SPEED_LEVELS[0]
        self.text_input.text = ""
        self.paused = False
        
        # Restart timers
        Clock.unschedule(self.update_timer)
        Clock.unschedule(self.update)
        Clock.unschedule(self.spawn_enemy)
        Clock.unschedule(self.spawn_power_up)
        Clock.schedule_interval(self.update_timer, 1.0)
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        Clock.schedule_interval(self.spawn_enemy, 2)
        Clock.schedule_interval(self.spawn_power_up, 15)
        Clock.schedule_once(self.set_focus, 0.1)

    def get_high_score(self):
        try:
            with open("D:\\Y1\\StudyY1\\TypingSurvival\\high_score.txt", "r") as file:
                return int(file.read())
        except FileNotFoundError:
            return 0
        except:
            return 0

    def set_high_score(self, score):
        try:
            with open("D:\\Y1\\StudyY1\\TypingSurvival\\high_score.txt", "w") as file:
                file.write(str(score))
            self.high_score_label.text = f"High Score: {score}"
        except Exception as e:
            print(f"Error saving high score: {e}")

class GameOverScreen(Screen):
    def __init__(self, screen_manager, **kwargs):
        super(GameOverScreen, self).__init__(**kwargs)
        self.screen_manager = screen_manager
        self.score = 0
        self.max_combo = 0

        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        
        game_over_label = Label(
            text="Game Over",
            font_size=48,
            size_hint=(1, 0.3)
        )
        
        # เพิ่ม layout สำหรับแสดงคะแนนและ combo
        stats_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.4))
        
        self.score_label = Label(
            text=f"Your Score: {self.score}",
            font_size=36,
            size_hint=(1, 0.5)
        )
        
        self.combo_label = Label(
            text=f"Max Combo: {self.max_combo}",
            font_size=30,
            size_hint=(1, 0.5),
            color=(1, 0.8, 0, 1)  # สีเหลืองทอง
        )
        
        stats_layout.add_widget(self.score_label)
        stats_layout.add_widget(self.combo_label)
        
        button_layout = BoxLayout(
            orientation='horizontal', 
            spacing=10,
            size_hint=(1, 0.2)
        )
        
        restart_button = Button(
            text="New Game",
            font_size=24,
            size_hint=(0.5, 1)
        )
        restart_button.bind(on_press=self.restart_game)
        
        home_button = Button(
            text="Home",
            font_size=24,
            size_hint=(0.5, 1)
        )
        home_button.bind(on_press=self.go_home)
        
        button_layout.add_widget(restart_button)
        button_layout.add_widget(home_button)
        
        layout.add_widget(game_over_label)
        layout.add_widget(stats_layout)
        layout.add_widget(button_layout)
        
        self.add_widget(layout)

    def go_home(self, instance):
        self.screen_manager.current = 'start'

    def restart_game(self, instance):
        game_screen = self.screen_manager.get_screen('game')
        game_screen.children[0].restart_game(None)
        self.screen_manager.current = 'game'

    def update_score_label(self):
        self.score_label.text = f"Your Score: {self.score}"
        self.combo_label.text = f"Max Combo: {self.max_combo}"

class BorderedLabel(BoxLayout):
    def __init__(self, text='', font_size=24, **kwargs):
        super(BorderedLabel, self).__init__(**kwargs)

        with self.canvas.before:
            Color(0.5, 0.5, 0.5, 1)
            self.border = Rectangle(pos=self.pos, size=self.size)

        self.label = Label(
            text=text,
            font_size=font_size,
            size_hint=(1, 1),
            color=(9, 0, 9, 9)
        )
        self.add_widget(self.label)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.border.pos = self.pos
        self.border.size = self.size

class StartScreen(Screen):
    def __init__(self, screen_manager, **kwargs):
        super(StartScreen, self).__init__(**kwargs)
        self.screen_manager = screen_manager

        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        
        title_label = BorderedLabel(
            text="TYPING-ATTACK",
            font_size=70,
            size_hint=(1, 0.4)
        )
        
        start_button = Button(
            text="Start Game",
            font_size=36,
            size_hint=(1, 0.2),
            color=(0, 0, 9, 1)
        )
        start_button.bind(on_press=self.start_game)
        
        high_score_button = Button(
            text="High Score",
            font_size=24,
            size_hint=(1, 0.1),
            color=(0, 6, 6, 1)
        )
        high_score_button.bind(on_press=self.view_high_score)
        
        volume_layout = BoxLayout(size_hint=(1, 0.1), spacing=5)
        
        volume_up_button = Button(
            text="Volume Up",
            font_size=24,
            color=(6, 0, 0, 1)
        )
        volume_up_button.bind(on_press=self.volume_up)
        volume_down_button = Button(
            text="Volume Down",
            font_size=24,
            color=(0, 1, 0, 1)
        )
        volume_down_button.bind(on_press=self.volume_down)
        
        volume_layout.add_widget(volume_up_button)
        volume_layout.add_widget(volume_down_button)
        
        layout.add_widget(title_label)
        layout.add_widget(start_button)
        layout.add_widget(high_score_button)
        layout.add_widget(volume_layout)
        
        self.add_widget(layout)

    def view_high_score(self, instance):
        self.screen_manager.current = 'high_score'

    def volume_up(self, instance):
        game_screen = self.screen_manager.get_screen('game').children[0]
        if hasattr(game_screen, 'sound') and game_screen.sound:
            game_screen.sound.volume = min(1, game_screen.sound.volume + 0.1)

    def volume_down(self, instance):
        game_screen = self.screen_manager.get_screen('game').children[0]
        if hasattr(game_screen, 'sound') and game_screen.sound:
            game_screen.sound.volume = max(0, game_screen.sound.volume - 0.1)

    def start_game(self, instance):
        self.screen_manager.current = 'game'
        Clock.schedule_once(lambda dt: self.screen_manager.get_screen('game').children[0].set_focus(None), 0.1)

class HighScoreScreen(Screen):
    def __init__(self, screen_manager, high_score=0, **kwargs):
        super(HighScoreScreen, self).__init__(**kwargs)
        self.screen_manager = screen_manager
        self.high_score = high_score

        # สร้าง main layout แนวตั้ง
        layout = BoxLayout(orientation='vertical', spacing=20, padding=40)
        
        # สร้าง title layout
        title_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.6))
        
        # Label สำหรับ title "HIGH SCORE"
        title_label = Label(
            text="HIGH SCORE",
            font_size=70,
            color=(1, 1, 0, 1),  # สีเหลือง
            size_hint=(1, 0.5)
        )
        
        # Label สำหรับแสดงคะแนน
        self.score_display = Label(
            text=f"{self.get_high_score()}",
            font_size=100,
            color=(1, 1, 1, 1),  # สีขาว
            size_hint=(1, 0.5)
        )
        
        title_layout.add_widget(title_label)
        title_layout.add_widget(self.score_display)
        
        # สร้างปุ่มกลับ
        back_button = Button(
            text="BACK",
            font_size=36,
            size_hint=(1, 0.2),
            background_color=(0.8, 0.2, 0.2, 1),  # สีแดงอ่อน
            color=(1, 1, 1, 1)  # สีขาว
        )
        back_button.bind(on_press=self.go_back)
        
        # เพิ่ม widgets เข้า layout หลัก
        layout.add_widget(title_layout)
        layout.add_widget(back_button)
        
        self.add_widget(layout)

    def update_high_score_display(self):
        # อัพเดทการแสดงผลคะแนนสูงสุด
        high_score = self.get_high_score()
        self.score_display.text = f"{high_score}"

    def on_pre_enter(self):
        # เรียกใช้เมื่อหน้าจอกำลังจะแสดง
        self.update_high_score_display()

    def get_high_score(self):
        file_path = "D:\\Y1\\StudyY1\\TypingSurvival\\high_score.txt"
        try:
            with open(file_path, "r") as file:
                high_score = int(file.read())
                return high_score
        except FileNotFoundError:
            print(f"High score file not found at {file_path}. Returning default high score (0).")
            return 0
        except Exception as e:
            print(f"An error occurred while reading the high score file: {e}")
            return 0

    def go_back(self, instance):
        self.screen_manager.current = 'start'

class TypingAttackApp(App):
    def build(self):
        screen_manager = ScreenManager()

        # Create and add screens
        start_screen = StartScreen(screen_manager, name='start')
        screen_manager.add_widget(start_screen)
        
        game_screen = Screen(name='game')
        game_screen.add_widget(TypingAttackGame(screen_manager))
        screen_manager.add_widget(game_screen)

        game_over_screen = GameOverScreen(screen_manager, name='game_over')
        screen_manager.add_widget(game_over_screen)
        
        high_score_screen = HighScoreScreen(screen_manager, name='high_score')
        screen_manager.add_widget(high_score_screen)

        screen_manager.current = 'start'
        Window.fullscreen = 'auto'
        
        return screen_manager

if __name__ == '__main__':
    TypingAttackApp().run()