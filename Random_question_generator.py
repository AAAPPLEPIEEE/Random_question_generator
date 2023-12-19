# -*- coding: utf-8 -*-
import docx
import random
import re # 導入正則表達式庫

def read_questions_from_docx(file_path):
    # 從 DOCX 檔案中讀取問題和選項
    doc = docx.Document(file_path) # 使用 python-docx 庫中的 Document 類來讀取 DOCX 文件
    questions = [] # 創建空列表來存放問題和選項
    current_question = None  # 紀錄當前的問題
    for para in doc.paragraphs:
        text = para.text.strip() # 獲取段落文本，並去除前後空格
        # 使用正則表達式匹配以數字開頭的行（包括兩位數）
        match = re.match(r'^(\d{1,2})\.(.*)', text) # 使用正則表達式檢查行是否符合題目格式
        if match:
            question_text = match.group(2).strip()  # 提取問題文本
            # 判斷是否有正確答案的標記(以括號內數字開頭的部分)
            answer_match = re.search(r'\(\s*\d+\s*\)', question_text) # 檢查問題文本中是否有答案標記
            correct_answer = None # 初始化正確答案
            if answer_match:
                correct_answer = int(answer_match.group().strip('()')) # 提取正確答案
                # 隱藏正確答案
                question_text = question_text.replace(answer_match.group(), '()')
            # 創建問題字典，並加入到問題列表中
            question = {
                'question': question_text,
                'options': [],
                'answer': correct_answer
            }
            questions.append(question) # 將問題添加到問題列表中
            current_question = question # 更新當前問題
        elif text and text.startswith(')'):
            if current_question:
                option = text[text.find(')') + 1:].strip()  # 提取選項文本
                current_question['options'].append(option) # 將選項添加到當前問題的選項列表中
                if text.startswith('('):
                    current_question['answer'] = int(text[1])  # 提取正確答案
    return questions # 返回問題列表

def select_random_questions(questions, num_questions=20):
    # 隨機選擇指定數量的問題
    return random.sample(questions, min(num_questions, len(questions))) # 使用 random.sample 方法從問題列表中選擇指定數量的問題

def conduct_exam(questions):
    # 進行考試並評分
    total_score = 0  # 初始化考試總分
    for i, question in enumerate(questions, 1):
        print(f"({i}) {question['question']}") # 顯示問題文本
        for idx, option in enumerate(question['options'], 1):
            print(f"    {idx}. {option}") # 顯示選項
        user_answer = input("Your answer (1/2/3/4): ") # 接收用戶的答案
        if user_answer.isdigit() and 1 <= int(user_answer) <= 4: # 確認用戶輸入是否為數字且在範圍內
            user_answer = int(user_answer)
            if user_answer == question['answer']: # 判斷用戶答案是否正確
                total_score += 5 # 更新總分
        else:
            print("Invalid input! Please enter a number between 1 and 4.")  # 輸入無效提示
    return total_score # 返回考試總分

def main():
    file_path = r'C:\Users\USER\Desktop\JOB\APR\c\PYTHON\RANDOM TEST\security_2.docx'  # 硬編碼的文件路徑
    questions = read_questions_from_docx(file_path)  # 讀取問題
    selected_questions = select_random_questions(questions, 20)  # 隨機選擇20題問題
    total_score = conduct_exam(selected_questions)  # 進行考試並評分
    print(f"Your total score is: {total_score}/100")  # 輸出總分

if __name__ == "__main__":
    main()
