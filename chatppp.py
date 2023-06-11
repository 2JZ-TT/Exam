import pandas as pd

# 12주차 레벤슈타인 거리를 계산하는 함수 참조.
def calc_distance(a, b):
    
    if a == b: return 0  # 두 문자열이 같으면 거리는 0을 반환.
    a_len = len(a)  # a길이.
    b_len = len(b)  # b길이.
    if a == "": return b_len  # a가 null"" b_len 반환.
    if b == "": return a_len  # b가 null"" a_len 반환.

    #  2차원 표 (a_len+1, b_len+1) 준비하기
    matrix = [[] for i in range(a_len+1)]
    for i in range(a_len+1):
        matrix[i] = [0 for j in range(b_len+1)]
    
    # matrix 를 0으로 초기와
    for i in range(a_len+1):
        matrix[i][0] = i
    for j in range(b_len+1):
        matrix[0][j] = j
    
    # 레벤슈타인 거리 계산
    for i in range(1, a_len+1):
        ac = a[i-1]
        for j in range(1, b_len+1):
            bc = b[j-1]
            cost = 0 if (ac == bc) else 1  # 두 문자가 같으면 cost는 0, 다르면 1
            matrix[i][j] = min([
                matrix[i-1][j] + 1,  # 삭제
                matrix[i][j-1] + 1,  # 삽입
                matrix[i-1][j-1] + cost  # 대체
            ])
    # 계산된 거리 반환
    return matrix[a_len][b_len]

# 챗봇 클래스를 정의.
class SimpleChatBot:
    # 초기화 메서드 >> questions  , answer filtpath 경로를 로드.
    def __init__(self, filepath):
        self.questions, self.answers = self.load_data(filepath)

    # load_data 메서드 >> CSV 파일에서 질문과 답변 데이터 열기
    def load_data(self, filepath):
        data = pd.read_csv(filepath)
        questions = data['Q'].tolist()
        answers = data['A'].tolist()
        return questions, answers

    # 입력 문장에 가장 잘 맞는 답변을 찾는 메서드, 입력 문장을 벡터화하고, 이를 기존 질문 벡터들과 비교하여 가장 높은 유사도를 가진 질문의 답변을 반환.
    def find_best_answer(self, input_sentence):
        # 입력 질문에 대하여 calc_distace 에 모두 대입하여 거리를 계산.
        distances = [calc_distance(input_sentence, question) for question in self.questions]
        # 가장 짧은 거리의 index를 찾아 best_match_index 저장.
        best_match_index = distances.index(min(distances))
        # 해당하는 index 의 answers 를 반환.
        return self.answers[best_match_index]

# 데이터 경로 지정.
filepath = 'ChatbotData.csv'
# 클래스 객체생성 매개변수 .
chatbot = SimpleChatBot(filepath)

# 'while 항상 true이며 입력에 대한 값이 종료 일때 break.
while True:
    # 콘솔에 키입력을 받아 input_sentec저장.
    input_sentence = input('You: ')
    # 키입력 값이 종료 이면 break. while 종료.
    if input_sentence.lower() == '종료':
        break
    #in 문을 거쳐 클래스의 메서드(매개변수) 호출
    response = chatbot.find_best_answer(input_sentence)
    #반환된 self.answers[best_match_index] 를 resopnse 로 저장되고 출력.
    print('Chatbot:', response)