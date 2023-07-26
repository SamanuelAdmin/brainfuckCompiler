from kivy.app import App

from kivy.lang import Builder
from kivy.core.window import Window

from kivy.properties import ObjectProperty

from kivy.uix.boxlayout import BoxLayout


Window.size = (600, 400)


Builder.load_string('''
<box>:

	code: code
	filename: filename

	orientation: 'vertical'

	TextInput:
		id: code
		text: '/*some code*/'

	BoxLayout:
		size_hint: 1, 0.1

		Button:
			text: 'save'
			size_hint: 0.3, 1
			on_press: root.save()

		BoxLayout:
			Label:
				size_hint: 0.2, 1
				text: 'File name: '

			TextInput:
				size_hint: 0.5, 1
				id: filename
				text: 'file.py'


''')


class box(BoxLayout):
	
	code = ObjectProperty()
	filename = ObjectProperty()

	def compile(self, text): 
		base = 'sp_ascii = [chr(i) for i in range(256)]\nindex = 0\narr = [0 for i in range(30000)]\n'

		sp_with_func = {
			'+': 'arr[index] += 1\n',
			'-': 'arr[index] -= 1\n',
			'<': 'index -= 1\n',
			'<': 'index += 1\n',
			'.': 'print(chr(arr[index]), end="")\n',
			'[': 'while arr[index] != 0:\n',
			',': 'arr[index] = sp_ascii.index(input()[0])\n'
		}

		if_tab = 0

		for byteindex in range(0, len(text)):
			try:
				byte_ = text[byteindex]

				if byte_ == '[':
					if if_tab > 0:
						t = ' ' * 4 * if_tab
						base += t
					base += sp_with_func[byte_]
					if_tab += 1

				elif byte_ == ']':
					if_tab -= 1
	
				else:
					if if_tab >= 0:
						base = base + ' ' * 4 * if_tab
					else:
						raise Exception('Tabulation error')
		
					base += sp_with_func[byte_]

			except KeyError:
				pass
			except Exception as error:
				print(error) #I hate nigga

		open(self.filename.text, 'w').write(base)

		print(chr(7))


	def save(self):
		self.compile(self.code.text)



class MainApp(App):

	def build(self):
	 	return box()


MainApp().run()
