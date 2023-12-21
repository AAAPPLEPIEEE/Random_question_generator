# -*- coding: utf-8 -*-
import docx
import random
import re 

def read_questions_from_docx(file_path):
    doc = docx.Document(file_path) 
    questions = [] 
    current_question = None  
    for para in doc.paragraphs:
        text = para.text.strip()
        match = re.match(r'^(\d{1,2})\.(.*)', text) 
        if match:
            question_text = match.group(2).strip()  
            answer_match = re.search(r'\(\s*\d+\s*\)', question_text) 
            correct_answer = None 
            if answer_match:
                correct_answer = int(answer_match.group().strip('()')) 
                question_text = question_text.replace(answer_match.group(), '()')
            question = {
                'question': question_text,
                'options': [],
                'answer': correct_answer
            }
            questions.append(question)
            current_question = question 
        elif text and text.startswith(')'):
            if current_question:
                option = text[text.find(')') + 1:].strip()  
                current_question['options'].append(option) 
                if text.startswith('('):
                    current_question['answer'] = int(text[1])  
    return questions 

def select_random_questions(questions, num_questions=20):
    return random.sample(questions, min(num_questions, len(questions))) 
def conduct_exam(questions):
    total_score = 0  
    for i, question in enumerate(questions, 1):
        print(f"({i}) {question['question']}") 
        for idx, option in enumerate(question['options'], 1):
            print(f"    {idx}. {option}") 
        user_answer = input("Your answer (1/2/3/4): ") 
        if user_answer.isdigit() and 1 <= int(user_answer) <= 4: 
            user_answer = int(user_answer)
            if user_answer == question['answer']: 
                total_score += 5 
        else:
            print("Invalid input! Please enter a number between 1 and 4.")  
    return total_score 

def main():
    file_path = r'C:\Users\USER\Desktop\JOB\APR\c\PYTHON\RANDOM TEST\security_2.docx'  
    questions = read_questions_from_docx(file_path)  
    selected_questions = select_random_questions(questions, 20)  
    total_score = conduct_exam(selected_questions)  
    print(f"Your total score is: {total_score}/100")  

if __name__ == "__main__":
    main()
