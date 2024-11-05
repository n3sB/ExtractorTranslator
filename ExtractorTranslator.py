import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import pytesseract
from langdetect import detect
from deep_translator import GoogleTranslator
import time

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

LANGUAGES = {
    'af': 'Afrikaans', 'sq': 'Albanian', 'am': 'Amharic', 'ar': 'Arabic', 'hy': 'Armenian', 'az': 'Azerbaijani',
    'eu': 'Basque', 'be': 'Belarusian', 'bn': 'Bengali', 'bs': 'Bosnian', 'bg': 'Bulgarian', 'ca': 'Catalan',
    'ceb': 'Cebuano', 'ny': 'Chichewa', 'zh-cn': 'Chinese (Simplified)', 'zh-tw': 'Chinese (Traditional)', 'co': 'Corsican',
    'hr': 'Croatian', 'cs': 'Czech', 'da': 'Danish', 'nl': 'Dutch', 'en': 'English', 'eo': 'Esperanto', 'et': 'Estonian',
    'tl': 'Filipino', 'fi': 'Finnish', 'fr': 'French', 'fy': 'Frisian', 'gl': 'Galician', 'ka': 'Georgian', 'de': 'German',
    'el': 'Greek', 'gu': 'Gujarati', 'ht': 'Haitian Creole', 'ha': 'Hausa', 'haw': 'Hawaiian', 'iw': 'Hebrew', 'hi': 'Hindi',
    'hmn': 'Hmong', 'hu': 'Hungarian', 'is': 'Icelandic', 'ig': 'Igbo', 'id': 'Indonesian', 'ga': 'Irish', 'it': 'Italian',
    'ja': 'Japanese', 'jw': 'Javanese', 'kn': 'Kannada', 'kk': 'Kazakh', 'km': 'Khmer', 'rw': 'Kinyarwanda', 'ko': 'Korean',
    'ku': 'Kurdish (Kurmanji)', 'ky': 'Kyrgyz', 'lo': 'Lao', 'la': 'Latin', 'lv': 'Latvian', 'lt': 'Lithuanian', 'lb': 'Luxembourgish',
    'mk': 'Macedonian', 'mg': 'Malagasy', 'ms': 'Malay', 'ml': 'Malayalam', 'mt': 'Maltese', 'mi': 'Maori', 'mr': 'Marathi',
    'mn': 'Mongolian', 'my': 'Myanmar (Burmese)', 'ne': 'Nepali', 'no': 'Norwegian', 'or': 'Odia (Oriya)', 'ps': 'Pashto',
    'fa': 'Persian', 'pl': 'Polish', 'pt': 'Portuguese', 'pa': 'Punjabi', 'ro': 'Romanian', 'ru': 'Russian', 'sm': 'Samoan',
    'gd': 'Scots Gaelic', 'sr': 'Serbian', 'st': 'Sesotho', 'sn': 'Shona', 'sd': 'Sindhi', 'si': 'Sinhala', 'sk': 'Slovak',
    'sl': 'Slovenian', 'so': 'Somali', 'es': 'Spanish', 'su': 'Sundanese', 'sw': 'Swahili', 'sv': 'Swedish', 'tg': 'Tajik',
    'ta': 'Tamil', 'tt': 'Tatar', 'te': 'Telugu', 'th': 'Thai', 'tr': 'Turkish', 'tk': 'Turkmen', 'uk': 'Ukrainian', 'ur': 'Urdu',
    'ug': 'Uyghur', 'uz': 'Uzbek', 'vi': 'Vietnamese', 'cy': 'Welsh', 'xh': 'Xhosa', 'yi': 'Yiddish', 'yo': 'Yoruba', 'zu': 'Zulu'
}

class AutocompleteCombobox(ttk.Combobox):
    def set_completion_list(self, completion_list):
        self._completion_list = sorted(completion_list)
        self._hits = []
        self.position = 0
        self.bind('<KeyRelease>', self.handle_keyrelease)
        self['values'] = self._completion_list
        
    def handle_keyrelease(self, event):
        typed = self.get()
        self._hits = [item for item in self._completion_list if item.lower().startswith(typed.lower())]
        self['values'] = self._hits

def extract_text_from_image(image_path):
    try:
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Image file not found at {image_path}") 
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray_image, config='--psm 6')
        return text
    except Exception as e:
        print(f"Error during text extraction: {e}")
        return ""

def translate_text(text, target_language_code, source_language_code):
    try:
        translated = GoogleTranslator(source=source_language_code, target=target_language_code).translate(text)
        return translated
    except Exception as e:
        print(f"Error during translation: {e}")
        return ""

def select_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        image_path_var.set(file_path)
        display_image(file_path)

def display_image(image_path):
    try:
        img = Image.open(image_path)
        img.thumbnail((200, 200))
        img = ImageTk.PhotoImage(img)
        image_label.config(image=img)
        image_label.image = img
        image_label.grid(row=2, column=0, columnspan=3, pady=5, sticky='nsew') 
    except Exception as e:
        messagebox.showerror("Error", f"Failed to display image: {e}")

def translate_and_export():
    image_path = image_path_var.get()
    target_language_name = language_var.get()
    target_language_code = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(target_language_name)]

    if not image_path:
        messagebox.showerror("Error", "Please select an image file")
        return

    if not target_language_name:
        messagebox.showerror("Error", "Please choose a target language")
        return

    start_time = time.time()
    extracted_text = extract_text_from_image(image_path)
    newExtracted_text = extracted_text.replace("\n", " ")

    if newExtracted_text:
        try:
            source_language_code = detect(newExtracted_text)
        except Exception as e:
            messagebox.showerror("Error", f"Could not detect language: {e}")
            return

        translated_text = translate_text(newExtracted_text, target_language_code, source_language_code)
        end_time = time.time()
        elapsed_time = end_time - start_time

        output_text = f"Execution Time: {elapsed_time:.2f} seconds"

        extracted_textbox.config(state=tk.NORMAL)
        extracted_textbox.delete(1.0, tk.END)
        extracted_textbox.insert(tk.END, newExtracted_text)
        extracted_textbox.config(state=tk.DISABLED)

        translated_textbox.config(state=tk.NORMAL)
        translated_textbox.delete(1.0, tk.END)
        translated_textbox.insert(tk.END, translated_text)
        translated_textbox.config(state=tk.DISABLED)

        time_textbox.config(state=tk.NORMAL)
        time_textbox.delete(1.0, tk.END)
        time_textbox.insert(tk.END, output_text)
        time_textbox.config(state=tk.DISABLED)

        overlay_text_on_image(image_path, translated_text)

    else:
        messagebox.showerror("Error", "No text extracted from the image.")

def clear_all():
    image_path_var.set("")
    language_var.set("")
    image_label.config(image="")
    extracted_textbox.config(state=tk.NORMAL)
    extracted_textbox.delete(1.0, tk.END)
    extracted_textbox.config(state=tk.DISABLED)
    translated_textbox.config(state=tk.NORMAL)
    translated_textbox.delete(1.0, tk.END)
    translated_textbox.config(state=tk.DISABLED)
    time_textbox.config(state=tk.NORMAL)
    time_textbox.delete(1.0, tk.END)
    time_textbox.config(state=tk.DISABLED)

def copy_extracted_text():
    extracted_text = extracted_textbox.get(1.0, tk.END)
    root.clipboard_clear()
    root.clipboard_append(extracted_text)

def copy_translated_text():
    translated_text = translated_textbox.get(1.0, tk.END)
    root.clipboard_clear()
    root.clipboard_append(translated_text)

root = tk.Tk()
root.title("Image Text Translator")
root.resizable(False, False) 

image_path_var = tk.StringVar()
language_var = tk.StringVar()

frame = ttk.Frame(root, padding=10)
frame.pack(fill=tk.BOTH, expand=True)

frame.grid_rowconfigure(1, weight=1)
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)
frame.grid_columnconfigure(2, weight=1)

upload_label = ttk.Label(frame, text="Upload Your Image")
upload_label.grid(row=0, column=0, pady=5, sticky='w')
upload_button = ttk.Button(frame, text="Browse", command=select_image)
upload_button.grid(row=0, column=2, pady=5, sticky='e')

image_path_entry = ttk.Entry(frame, textvariable=image_path_var, width=50)
image_path_entry.grid(row=1, column=0, columnspan=3, pady=5, sticky='ew')

image_label = ttk.Label(frame)
image_label.grid(row=2, column=0, columnspan=3, pady=5, sticky='nsew')

language_label = ttk.Label(frame, text="Translate To")
language_label.grid(row=3, column=0, pady=5, sticky='w')
autocomplete_combobox = AutocompleteCombobox(frame, textvariable=language_var)
autocomplete_combobox.set_completion_list(list(LANGUAGES.values()))
autocomplete_combobox.grid(row=3, column=1, pady=5, sticky='ew')

translate_button = ttk.Button(frame, text="Translate & Export", command=translate_and_export)
translate_button.grid(row=4, column=0, columnspan=3, pady=10, sticky='ew')

extracted_text_label = ttk.Label(frame, text="Extracted Text")
extracted_text_label.grid(row=5, column=0, pady=5, sticky='w')
extracted_textbox = tk.Text(frame, wrap=tk.WORD, height=10)
extracted_textbox.grid(row=6, column=0, pady=10, sticky='nsew')
extracted_textbox.config(state=tk.DISABLED)

translated_text_label = ttk.Label(frame, text="Translated Text")
translated_text_label.grid(row=5, column=2, pady=5, sticky='w')
translated_textbox = tk.Text(frame, wrap=tk.WORD, height=10)
translated_textbox.grid(row=6, column=2, pady=10, sticky='nsew')
translated_textbox.config(state=tk.DISABLED)

time_textbox = tk.Text(frame, wrap=tk.WORD, height=1)
time_textbox.grid(row=7, column=0, columnspan=3, pady=10, sticky='nsew')
time_textbox.config(state=tk.DISABLED)

copy_extracted_button = ttk.Button(frame, text="Copy Extracted", command=copy_extracted_text)
copy_extracted_button.grid(row=8, column=0, pady=5, sticky='ew')

copy_translated_button = ttk.Button(frame, text="Copy Translated", command=copy_translated_text)
copy_translated_button.grid(row=8, column=2, pady=5, sticky='ew')

clear_button = ttk.Button(frame, text="Clear All", command=clear_all)
clear_button.grid(row=9, column=0, columnspan=3, pady=10, sticky='ew')

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

frame.grid(row=0, column=0, sticky='nsew')

root.mainloop()
