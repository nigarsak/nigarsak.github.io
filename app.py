from flask import Flask, render_template, request, jsonify, session
import json
import random
import time
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'kelime_oyunu_secret_key_2024'

# Kelime havuzu (örnek)
DEFAULT_WORDS = [
    {"word": "mecaz", "meaning": "Bir kelimenin veya ifadenin gerçek anlamı dışında, benzetme veya başka bir ilişki yoluyla kullanılması."},
    {"word": "deyim", "meaning": "Genellikle gerçek anlamından uzaklaşarak kendine özgü bir anlam taşıyan, kalıplaşmış söz öbeği."},
    {"word": "atasözü", "meaning": "Uzun deneyim ve gözlemlere dayanarak oluşmuş, topluma öğüt veren, yol gösteren özlü söz."},
    {"word": "betimleme", "meaning": "Varlıkları, nesneleri veya olayları, okuyucunun zihninde canlanacak şekilde sözcüklerle resmetme."},
    {"word": "öznel", "meaning": "Kişisel görüşe, duyguya veya zevke dayanan, kişiden kişiye değişebilen düşünce veya yargı."},
    {"word": "nesnel", "meaning": "Kişiden bağımsız, kanıtlanabilir gerçeklere dayanan, herkes için geçerli olan bilgi veya yargı."},
    {"word": "uyak", "meaning": "Dize sonlarında veya aralarında bulunan, görev ve anlamları farklı sözcükler arasındaki ses benzerliği (kafiye)."},
    {"word": "ikileme", "meaning": "Anlamı pekiştirmek, güçlendirmek veya farklı bir anlam katmak için iki kelimenin arka arkaya kullanılması."},
    {"word": "terim", "meaning": "Bir bilim, sanat veya meslek dalına özgü, özel ve belirli bir anlam taşıyan kelime."},
    {"word": "anlam", "meaning": "Bir kelimenin, işaretin veya ifadenin temsil ettiği düşünce, fikir veya kavram."},
    {"word": "sözcük", "meaning": "Dildeki en küçük anlamlı birim; kelime."},
    {"word": "eş anlamlı", "meaning": "Yazılışları farklı olsa da aynı veya çok yakın anlamı taşıyan kelimeler."},
    {"word": "zıt anlamlı", "meaning": "Anlamca birbirinin karşıtı olan kelimeler (karşıt anlamlı)."},
    {"word": "köken", "meaning": "Bir kelimenin veya şeyin çıktığı, dayandığı yer; asıl başlangıç."},
    {"word": "çekim eki", "meaning": "Kelimenin anlamını değiştirmeyen, ancak görevini ve yerini belirleyen ek (çoğul, hâl, zaman ekleri vb.)."},
    {"word": "yapım eki", "meaning": "Eklendiği kelimenin anlamını veya türünü değiştirerek yeni bir kelime oluşturan ek."},
    {"word": "fonetik", "meaning": "Dilin seslerini inceleyen bilim dalı; ses bilimiyle ilgili olan."},
    {"word": "morfoloji", "meaning": "Kelime yapısını ve kelimelerin biçimsel özelliklerini inceleyen bilim dalı (biçim bilimi)."},
    {"word": "anlatım", "meaning": "Düşünceleri, duyguları veya olayları sözlü ya da yazılı olarak ifade etme biçimi."},
    {"word": "üslup", "meaning": "Bir yazarın veya konuşmacının anlatım tarzı, dili kullanma biçimi (stil)."},
    {"word": "nüans", "meaning": "Birbirine yakın şeyler arasındaki ince fark, küçük ayrım."},
    {"word": "tasvir", "meaning": "Bir şeyi sözle veya yazıyla somut biçimde anlatma, betimleme."},
    {"word": "mukayese", "meaning": "İki veya daha fazla şeyi benzerlikleri ve farklılıkları yönünden karşılaştırma."},
    {"word": "özgün", "meaning": "Kendine has, orijinal, başkasına benzemeyen niteliklere sahip."},
    {"word": "muhteva", "meaning": "Bir yazının, konuşmanın veya eserin içeriği, kapsamı."}
]

WORDS_FILE = 'kelime_havuzu.json'
LEADERBOARD_FILE = 'liderlik_tablosu.json'

def load_words():
    """Kelime havuzunu dosyadan yükler veya varsayılanı kullanır."""
    if os.path.exists(WORDS_FILE):
        try:
            with open(WORDS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return DEFAULT_WORDS
    return DEFAULT_WORDS

def load_leaderboard():
    """Liderlik tablosunu dosyadan yükler."""
    if os.path.exists(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_leaderboard(leaderboard):
    """Liderlik tablosunu dosyaya kaydeder."""
    with open(LEADERBOARD_FILE, 'w', encoding='utf-8') as f:
        json.dump(leaderboard, f, ensure_ascii=False, indent=4)

def build_questions(word_list, count):
    """Oyun için soru ve seçenekleri oluşturur."""
    if count > len(word_list):
        count = len(word_list)
    
    selected_words = random.sample(word_list, count)
    all_meanings = [w['meaning'] for w in word_list]
    questions = []
    
    for item in selected_words:
        correct_meaning = item['meaning']
        other_meanings = [m for m in all_meanings if m != correct_meaning]
        wrong_meanings = random.sample(other_meanings, min(3, len(other_meanings)))
        
        options = [correct_meaning] + wrong_meanings
        random.shuffle(options)
        
        questions.append({
            'word': item['word'],
            'correct': correct_meaning,
            'options': options
        })
    
    return questions

@app.route('/')
def index():
    """Ana sayfa"""
    word_count = len(load_words())
    return render_template('index.html', word_count=word_count)

@app.route('/start_game', methods=['POST'])
def start_game():
    """Oyunu başlatır"""
    data = request.get_json()
    student_name = data.get('student_name', 'İsimsiz')
    school_name = data.get('school_name', 'İsimsiz')
    question_count = int(data.get('question_count', 10))
    
    word_list = load_words()
    questions = build_questions(word_list, question_count)
    
    # Session'da oyun bilgilerini sakla
    session['student_name'] = student_name
    session['school_name'] = school_name
    session['questions'] = questions
    session['current_question'] = 0
    session['score'] = 0
    session['start_time'] = time.time()
    
    return jsonify({'success': True, 'total_questions': len(questions)})

@app.route('/get_question')
def get_question():
    """Mevcut soruyu döndürür"""
    if 'questions' not in session:
        return jsonify({'error': 'Oyun başlatılmamış'})
    
    current = session['current_question']
    questions = session['questions']
    
    if current >= len(questions):
        return jsonify({'game_finished': True})
    
    question = questions[current]
    return jsonify({
        'word': question['word'],
        'options': question['options'],
        'current': current + 1,
        'total': len(questions),
        'score': session['score']
    })

@app.route('/answer', methods=['POST'])
def answer():
    """Cevabı kontrol eder"""
    if 'questions' not in session:
        return jsonify({'error': 'Oyun başlatılmamış'})
    
    data = request.get_json()
    selected_answer = data.get('answer')
    
    current = session['current_question']
    questions = session['questions']
    question = questions[current]
    
    is_correct = selected_answer == question['correct']
    if is_correct:
        session['score'] += 1
    
    session['current_question'] += 1
    
    # Oyun bitti mi kontrol et
    game_finished = session['current_question'] >= len(questions)
    
    result = {
        'correct': is_correct,
        'correct_answer': question['correct'],
        'score': session['score'],
        'game_finished': game_finished
    }
    
    if game_finished:
        # Skoru kaydet
        end_time = time.time()
        duration = end_time - session['start_time']
        save_score(session['student_name'], session['score'], len(questions), duration)
        result['final_score'] = session['score']
        result['total_questions'] = len(questions)
        result['duration'] = f"{duration:.2f}"
    
    return jsonify(result)

@app.route('/leaderboard')
def leaderboard():
    """Liderlik tablosu sayfası"""
    leaderboard_data = load_leaderboard()[:10]  # İlk 10'u göster
    return render_template('leaderboard.html', leaderboard=leaderboard_data)

def save_score(name, score, total, duration):
    """Skoru liderlik tablosuna kaydeder"""
    leaderboard = load_leaderboard()
    entry = {
        'name': name,
        'score': score,
        'total': total,
        'duration': f"{duration:.2f} saniye",
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    leaderboard.append(entry)
    leaderboard.sort(key=lambda x: x['score'] / x['total'], reverse=True)
    save_leaderboard(leaderboard)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)