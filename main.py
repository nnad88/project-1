import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color
import random

class TestApp(App):
    theme = ""
    num_questions = 0
    current_question = 0
    questions = []
    theme_button = None
    blue_color = (0.082, 0.667, 1, 1)

    def build(self):
        self.layout = BoxLayout(orientation='vertical', spacing=5)
        self.label = Label(text='Selecciona un tema:')
        self.layout.add_widget(self.label)

        themes = ['Examen General', 'Meteorologia', 'Navegacion']
        for theme in themes:
            button = Button(text=theme, background_color = self.blue_color, background_normal = '')
            button.bind(on_press=self.theme_selected)
            self.layout.add_widget(button)
        return self.layout

    def theme_selected(self, instance):
        self.theme = instance.text
        self.theme_button = instance  # Store the current theme button
        self.layout.clear_widgets()

        # Recreate and add the label
        self.label = Label(text=f'¿Cuántas preguntas para {self.theme}?')
        self.layout.add_widget(self.label)

        num_buttons = [5, 20, 30]

        # Create a vertical BoxLayout to hold the buttons with spacing
        button_layout = BoxLayout(orientation='vertical', spacing=5)

        for num in num_buttons:
            button = Button(text=str(num), background_normal='', background_color=self.blue_color)
            with button.canvas:
                Color(1, 1, 1, 1)  # Set the font color to white
            button.bind(on_press=self.start_exam)
            button_layout.add_widget(button)

        self.layout.add_widget(button_layout)

    def start_exam(self, instance):
        self.num_questions = int(instance.text)
        self.layout.clear_widgets()
        self.load_questions()
        self.current_question = 0
        self.correct_answers = 0
        self.results = []  # To store results of each question
        self.display_question()

    def load_questions(self):
        self.questions = {
            'Meteorologia': [
                {
                    'question': '¿El aire caliente tiende a subir?',
                    'options': ['a. Si', 'b. No'],
                    'correct_answer': 0
                },
                {
                    'question': '¿Qué es la cizalladura del viento?',
                    'options': ['a. Cambio de dirección y velocidad del viento con la altura', 'b. Una tormenta'],
                    'correct_answer': 0
                }
            ],
            'Navegacion': [
                {
                    'question': '¿La 1encuentra en el norte geográfico?',
                    'options': ['a. Si', 'b. No'],
                    'correct_answer': 0
                },
                {
                    'question': '¿La la2e en grados norte o sur del ecuador?',
                    'options': ['a. Norte', 'b. Sur'],
                    'correct_answer': 1
                },
                {
                    'question': '¿La lat3 mide en grados norte o sur del ecuador?',
                    'options': ['a. Norte', 'b. Sur'],
                    'correct_answer': 1
                },
                {
                    'question': '¿La la4e mide en grados norte o sur del ecuador?',
                    'options': ['a. Norte', 'b. Sur'],
                    'correct_answer': 1
                },
                {
                    'question': '¿La lat5de en grados norte o sur del ecuador?',
                    'options': ['a. Norte', 'b. Sur'],
                    'correct_answer': 1
                },
                {
                    'question': '¿La latitud se mide en grados norte o sur del ecuador?',
                    'options': ['a. Norte', 'b. Sur'],
                    'correct_answer': 1
                }
            ]
        }
        if self.theme == 'Examen General':
            all_questions = []
            for theme, theme_questions in self.questions.items():
                all_questions.extend(theme_questions)
            self.questions_for_theme = random.sample(all_questions, self.num_questions)
        else:
            self.questions_for_theme = random.sample(self.questions[self.theme], self.num_questions)

    def display_question(self):
        if self.current_question < self.num_questions:
            question_data = self.questions_for_theme[self.current_question]
            question_text = question_data['question']
            options = question_data['options']

            self.layout.clear_widgets()
            self.layout.add_widget(Label(text=question_text))

            grid = GridLayout(cols=1, spacing=10)  # Add spacing here
            for i, option in enumerate(options):
                button = Button(text=option, background_normal='', background_color=self.blue_color,
                                on_press=lambda instance, i=i: self.on_answer(i))
                grid.add_widget(button)
            self.layout.add_widget(grid)
        else:
            self.evaluate_results()

    def on_answer(self, selected_option):
        correct_answer = self.questions_for_theme[self.current_question]['correct_answer']
        is_correct = selected_option == correct_answer
        self.results.append((self.questions_for_theme[self.current_question]['question'], selected_option, correct_answer, is_correct))
        if is_correct:
            self.correct_answers += 1

        self.current_question += 1
        self.display_question()

    def evaluate_results(self):
        result = "Aprobado" if self.correct_answers / self.num_questions >= 0.8 else "Reprobado"

        result_text = f"Resultado: {result}\nRespuestas correctas: {self.correct_answers}/{self.num_questions}"
        details_text = ""

        for index, (question, selected_option, correct_option, is_correct) in enumerate(self.results, 1):
            details_text += f"{index}. {question}\n"
            details_text += f"{'Correcto' if is_correct else 'Incorrecto'}\n"
            details_text += f"Respuesta dada: {'a. Si' if selected_option == 0 else 'b. No'}\n"
            details_text += f"Respuesta correcta: {'a. Si' if correct_option == 0 else 'b. No'}\n\n"

        self.layout.clear_widgets()

        result_section_height = 0.15
        button_height = 0.15
        details_section_height = 1 - (result_section_height + button_height)

        result_label = Label(
            text=result_text,
            size_hint_y=None,
            height=100  # Set a fixed height for the Label (adjust as needed)
        )
        self.layout.add_widget(result_label)

        # Calculate the height of the details section
        details_height = self.root.height * details_section_height

        # Create a ScrollView for the details section
        details_scroll_view = ScrollView(size_hint=(1, None), height=details_height)
        details_label = Label(
            text=details_text,
            markup=True,
            size_hint_y=None,
            height=details_height
        )
        details_label.bind(texture_size=details_label.setter('size'))
        details_scroll_view.add_widget(details_label)
        self.layout.add_widget(details_scroll_view)

        restart_button = Button(
            text="Hacer otro examen",
            size_hint_y=None,
            height=button_height * self.root.height,
            background_color = self.blue_color,
            background_normal = ''
        )
        restart_button.bind(on_press=self.restart_exam)
        self.layout.add_widget(restart_button)

    def restart_exam(self, instance):
        # Clear the results and go back to theme selection
        self.layout.clear_widgets()
        self.label = Label(text='Selecciona un tema:')
        self.layout.add_widget(self.label)

        themes = ['Examen General', 'Meteorologia', 'Navegacion']
        for theme in themes:
            button = Button(text=theme, background_color = self.blue_color, background_normal = '')
            button.bind(on_press=self.theme_selected)
            self.layout.add_widget(button)


if __name__ == '__main__':
    TestApp().run()
