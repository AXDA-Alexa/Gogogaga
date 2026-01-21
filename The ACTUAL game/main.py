import arcade
from pathlib import Path
import time

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Sigma Joc"

# Constante pentru player
GRAVITY = 1.0
PLAYER_START_X = 65
PLAYER_START_Y = 256
PLAYER_MOVE_SPEED = 4.5
PLAYER_JUMP_SPEED = 10


class MainWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.tile_map = None
        self.scene = None
        self.player_list = arcade.SpriteList()
        self.player = None
        self.physics_engine = None
        self.npc = None

        # ----DIALOG-----
        self.show_dialog = False
        self.dialog_text = ""
        self.options = []
        self.dialog_state = "start"
        self.player_name = ""
        self.input_mode = False
        self.input_text = ""

        # Variabilă pentru a ști dacă putem vorbi cu NPC-ul
        self.can_talk = False

        # Cursor blink variabile
        self.cursor_visible = True
        self.last_cursor_toggle = time.time()
        self.cursor_blink_interval = 0.5  # secunde

    def setup(self):
        # --- Tile map și scene ---
        map_path = Path(__file__).parent / "First_map.tmx"
        self.tile_map = arcade.load_tilemap(str(map_path))
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        floor_list = self.scene.get_sprite_list("floor")
        car_list = self.scene.get_sprite_list("car")

        collision_list = arcade.SpriteList()
        collision_list.extend(floor_list)
        collision_list.extend(car_list)

        # --- Player setup ---
        self.player = arcade.AnimatedWalkingSprite()
        self.player.center_x = PLAYER_START_X
        self.player.center_y = PLAYER_START_Y

        assets_path = Path(__file__).parent / "assets"

        # Idle / stand right texture
        idle_texture = arcade.load_texture(str(assets_path / "Carmen_stand_right.png"))
        self.player.textures.append(idle_texture)
        self.player.stand_right_textures = [idle_texture]

        # Walk right
        self.player.walk_right_textures = [
            arcade.load_texture(str(assets_path / "Carmenwalk.png")),
            arcade.load_texture(str(assets_path / "Carmen_run.png"))
        ]

        # Walk left
        self.player.walk_left_textures = [
            arcade.load_texture(str(assets_path / "Carmen_walk_left.png")),
            arcade.load_texture(str(assets_path / "Carmen_run_left.png"))
        ]

        # Stand left
        self.player.stand_left_textures = [
            arcade.load_texture(str(assets_path / "Carmenstd_left.png"))
        ]

        # Jump right
        self.player.jump_right_textures = [
            arcade.load_texture(str(assets_path / "Carmen_jump.png"))
        ]

        # Jump left
        self.player.jump_left_textures = [
            arcade.load_texture(str(assets_path / "Carmen_jumping_left.png"))
        ]

        self.player.state = arcade.FACE_RIGHT

        self.player.scale = 1.0
        self.player_list.append(self.player)

        # ----NPC----
        npc_texture = arcade.load_texture(str(assets_path / "npc.png"))
        self.npc = arcade.Sprite()
        self.npc.texture = npc_texture
        self.npc.center_x = 515
        self.npc.center_y = 200
        self.npc.scale = 1.0
        self.scene.add_sprite("floor", self.npc)
        collision_list.append(self.npc)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player,
            collision_list,
            gravity_constant=GRAVITY
        )

        self.scene.add_sprite("Carmen", self.player)

    def on_draw(self):
        print("DEBUG: A intrat în on_draw()")
        self.clear()
        if self.scene:
            self.scene.draw()

        # Dialog
        if self.can_talk and not self.show_dialog:
            arcade.draw_text("Press E to talk",
                             self.player.center_x - 70, self.player.center_y + 50,
                             arcade.color.LIGHT_CARMINE_PINK, 30)

        # Dialog
        if self.show_dialog:
            print(f"DEBUG: show_dialog în on_draw = {self.show_dialog}")

            arcade.draw_lrbt_rectangle_filled(50, 950, 10, 150, arcade.color.WHITE_SMOKE)
            arcade.draw_text(self.dialog_text, 60, 130, arcade.color.BLACK, 18, width=880)
            print("DEBUG: Desenează dialogul cu text:", self.dialog_text)

            for i, option in enumerate(self.options):
                arcade.draw_text(f"{i + 1}. {option}", 70, 110 - i * 25, arcade.color.BLUE, 16)

            if self.input_mode:
                box_x, box_y = 60, 40
                box_width, box_height = 400, 30

                # Fundal casetă input (desenat primul)
                arcade.draw_lrbt_rectangle_filled(
                    left=box_x,
                    right=box_x + box_width,
                    bottom=box_y,
                    top=box_y + box_height,
                    color=arcade.color.LIGHT_GRAY
                )

                # Text input
                text_obj = arcade.Text(self.input_text, box_x + 5, box_y + 5, arcade.color.BLACK, 20)
                text_obj.draw()

                # Contur casetă input (desenat ultimul)
                arcade.draw_lrbt_rectangle_outline(
                    left=box_x,
                    right=box_x + box_width,
                    bottom=box_y,
                    top=box_y + box_height,
                    color=arcade.color.BLACK
                )

                # Cursor blink
                current_time = time.time()
                if current_time - self.last_cursor_toggle > self.cursor_blink_interval:
                    self.cursor_visible = not self.cursor_visible
                    self.last_cursor_toggle = current_time

                if self.cursor_visible:
                    cursor_x = box_x + 5 + text_obj.content_width + 2
                    cursor_y_bottom = box_y + 5
                    cursor_y_top = cursor_y_bottom + 20
                    arcade.draw_line(cursor_x, cursor_y_bottom, cursor_x, cursor_y_top, arcade.color.BLACK, 2)

    def on_update(self, delta_time):
        if self.physics_engine:
            self.physics_engine.update()

        if self.player:
            self.player.update()
            self.player.update_animation(delta_time)

        # Limitează poziția playerului să rămână în ecran
        self.player.center_x = max(self.player.width // 2,
                                   min(self.player.center_x, SCREEN_WIDTH - self.player.width // 2))
        self.player.center_y = max(self.player.height // 2,
                                   min(self.player.center_y, SCREEN_HEIGHT - self.player.height // 2))

        # Verifică dacă player-ul este aproape de NPC (distanta ajustabilă)
        distance = arcade.get_distance_between_sprites(self.player, self.npc)
        self.can_talk = distance < 100
        print(f"Distanța: {distance}, can_talk: {self.can_talk}")

    def on_key_press(self, key, modifiers):
        print(f"Tasta apăsată: {key}, can_talk={self.can_talk}, show_dialog={self.show_dialog}")
        print("DEBUG: A intrat în dialog!")
        if key == arcade.key.E and self.can_talk and not self.show_dialog:
            self.dialog_state = "start"
            self.show_dialog = True
            self.update_dialog()
            return

        if self.show_dialog:
            if self.input_mode:
                if key == arcade.key.BACKSPACE:
                    self.input_text = self.input_text[:-1]
                elif key == arcade.key.ENTER or key == arcade.key.RETURN:
                    self.player_name = self.input_text.strip()
                    self.input_mode = False
                    self.dialog_state = "after_name"
                    self.update_dialog()
                else:
                    # Acceptă litere, cifre și simboluri standard ASCII
                    if 32 <= key <= 126:
                        self.input_text += chr(key)
                return

            if key in [arcade.key.KEY_1, arcade.key.KEY_2, arcade.key.KEY_3]:
                option = key - arcade.key.KEY_1
                if option < len(self.options):
                    self.process_choice(option)
                return

            if key == arcade.key.E:
                self.show_dialog = False
                return

        # Mișcare player când nu e dialog
        if not self.show_dialog:
            if key == arcade.key.D:
                self.player.change_x = PLAYER_MOVE_SPEED
                self.player.state = arcade.FACE_RIGHT
            elif key == arcade.key.A:
                self.player.change_x = -PLAYER_MOVE_SPEED
                self.player.state = arcade.FACE_LEFT
            elif key == arcade.key.SPACE:
                if self.physics_engine and self.physics_engine.can_jump():
                    self.player.change_y = PLAYER_JUMP_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.D or key == arcade.key.A:
            self.player.change_x = 0

    def update_dialog(self):
        if self.dialog_state == "start":
            self.dialog_text = "Oh, you are new here... Ah, I forgot your name. Can you tell me?"
            print("DEBUG: dialog_text setat la:", self.dialog_text)
            self.options = ["Type your name"]
            self.input_mode = True
            self.input_text = ""
        elif self.dialog_state == "after_name":
            self.dialog_text = f"Ah, {self.player_name}, nice to meet you! Are you the new student?"
            self.options = ["Yes", "No"]
            self.input_mode = False
        elif self.dialog_state == "student_answer_yes":
            self.dialog_text = f"Great! {self.player_name}, you have really good equipment."
            self.options = ["Ask about mission", "Ask your name", "Quit"]
            self.input_mode = False
        elif self.dialog_state == "student_answer_no":
            self.dialog_text = "What a liar... Don't try to fool me, kiddo."
            self.options = ["Ask about mission", "Ask your name", "Quit"]
            self.input_mode = False
        elif self.dialog_state == "ask_mission":
            self.dialog_text = "Your mission is to save the world from the invading robots!"
            self.options = ["Ask your name", "Quit"]
            self.input_mode = False
        elif self.dialog_state == "ask_npc_name":
            self.dialog_text = "My name is Red. I'm here to guide you."
            self.options = ["Ask about mission", "Quit"]
            self.input_mode = False
        elif self.dialog_state == "quit":
            self.dialog_text = "Goodbye! Come back anytime."
            self.options = []
            self.show_dialog = False
            self.input_mode = False

    def process_choice(self, choice):
        if self.dialog_state == "after_name":
            if choice == 0:
                self.dialog_state = "student_answer_yes"
            elif choice == 1:
                self.dialog_state = "student_answer_no"
            self.update_dialog()
        elif self.dialog_state in ["student_answer_yes", "student_answer_no"]:
            if choice == 0:
                self.dialog_state = "ask_mission"
            elif choice == 1:
                self.dialog_state = "ask_npc_name"
            elif choice == 2:
                self.dialog_state = "quit"
            self.update_dialog()
        elif self.dialog_state == "ask_mission":
            if choice == 0:
                self.dialog_state = "ask_npc_name"
            elif choice == 1:
                self.dialog_state = "quit"
            self.update_dialog()
        elif self.dialog_state == "ask_npc_name":
            if choice == 0:
                self.dialog_state = "ask_mission"
            elif choice == 1:
                self.dialog_state = "quit"
            self.update_dialog()


def main():
    window = MainWindow()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
