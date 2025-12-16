import random
import json
import time
import os
from datetime import datetime

# --- KELİME HAVUZU (Örnek) ---
# JSON dosyasından kelime yükleyemezseniz bu örnek havuz kullanılır.
# Gerçek kelime havuzunu 'kelime_havuzu.json' dosyasına kaydedebilirsiniz.
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
    {"word": "anlam", "meaning": "Bir kelimenin, işaretin veya ifadenin temsil ettiği düşünce, fikir veya kavram."}
]

WORDS_FILE = 'kelime_havuzu.json'
LEADERBOARD_FILE = 'liderlik_tablosu.json'

def load_words():
    """Kelime havuzunu dosyadan yükler veya varsayılanı kullanır."""
    if os.path.exists(WORDS_FILE):
        try:
            with open(WORDS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Hata: Kelime havuzu dosyası yüklenemedi ({e}). Varsayılan havuz kullanılıyor.")
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
    
    # Karıştırılmış kelime havuzundan gerekli sayıda kelime seçilir
    selected_words = random.sample(word_list, count)
    all_meanings = [w['meaning'] for w in word_list]
    
    questions = []
    for item in selected_words:
        correct_meaning = item['meaning']
        
        # Doğru anlam dışındaki anlamlar
        other_meanings = [m for m in all_meanings if m != correct_meaning]
        
        # 3 yanlış anlam seçilir
        wrong_meanings = random.sample(other_meanings, min(3, len(other_meanings)))
        
        # Seçenekler oluşturulur ve karıştırılır
        options = [correct_meaning] + wrong_meanings
        random.shuffle(options)
        
        questions.append({
            'word': item['word'],
            'correct': correct_meaning,
            'options': options
        })
    
    return questions

def display_question(q, current_q, total_q, score):
    """Soruyu ve seçenekleri ekrana yazdırır."""
    print("\n" + "-"*50)
    print(f"❓ Soru {current_q}/{total_q} | Puan: {score}")
    print(f"\n** \"{q['word']}\" kelimesinin anlamı hangisidir? **")
    
    # Seçenekleri numaralandırarak yazdırır
    for i, option in enumerate(q['options'], 1):
        print(f"  {i}. {option}")
    print("-" * 50)

def get_user_answer(option_count):
    """Kullanıcıdan geçerli bir cevap (sayı) alır."""
    while True:
        try:
            choice = input(f"Cevabınız (1-{option_count}) veya (q)uit: ").strip().lower()
            if choice == 'q':
                return 'quit'
            
            choice_int = int(choice)
            if 1 <= choice_int <= option_count:
                return choice_int
            else:
                print(f"Geçersiz giriş. Lütfen 1 ile {option_count} arasında bir sayı girin.")
        except ValueError:
            print("Geçersiz giriş. Lütfen bir sayı girin.")

def play_game(word_list):
    """Oyunun ana döngüsünü çalıştırır."""
    print("🌟 Kelime & Anlam Eşleştirme Oyunu Başlıyor!")
    
    student_name = input("Öğrenci Adınız: ").strip() or "İsimsiz"
    school_name = input("Okulunuz: ").strip() or "İsimsiz"
    
    while True:
        try:
            q_count_input = input(f"Soru sayısı ({len(word_list)}'e kadar): ").strip() or "10"
            q_count = int(q_count_input)
            if 1 <= q_count <= len(word_list):
                break
            else:
                print(f"Lütfen 1 ile {len(word_list)} arasında bir sayı girin.")
        except ValueError:
            print("Geçersiz giriş. Lütfen bir sayı girin.")
    
    score = 0
    questions = build_questions(word_list, q_count)
    
    # Zamanlayıcı başlatılır
    start_time = time.time()
    
    for i, q in enumerate(questions):
        display_question(q, i + 1, q_count, score)
        
        answer = get_user_answer(len(q['options']))
        if answer == 'quit':
            print("\n❌ Oyundan vazgeçildi.")
            return
        
        chosen_meaning = q['options'][answer - 1]
        if chosen_meaning == q['correct']:
            score += 1
            print("✅ Doğru!")
        else:
            print(f"❌ Yanlış! Doğru cevap: **{q['correct']}**")
        
        # Her sorudan sonra kısa bir bekleme
        time.sleep(0.5)
    
    # Oyun bitiş zamanı
    end_time = time.time()
    total_time = end_time - start_time
    
    # --- Oyun Sonucu ---
    print("\n" + "="*50)
    print("🏆 OYUN BİTTİ!")
    print(f"Öğrenci: {student_name}")
    print(f"Okul: {school_name}")
    print(f"Puanınız: {score}/{q_count}")
    print(f"Süre: {total_time:.2f} saniye")
    print("="*50)
    
    # Skor kaydetme
    save_score(student_name, school_name, score, q_count, total_time)

def save_score(name, school, score, total, duration):
    """Skoru liderlik tablosuna kaydeder."""
    leaderboard = load_leaderboard()
    
    entry = {
        'name': name,
        'school': school,
        'score': score,
        'total': total,
        'duration': f"{duration:.2f} saniye",
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    leaderboard.append(entry)
    
    # Skor/Toplam oranına göre sıralama
    leaderboard.sort(key=lambda x: x['score'] / x['total'], reverse=True)
    
    save_leaderboard(leaderboard)
    print("🎉 Skorunuz Liderlik Tablosuna eklendi.")

def view_leaderboard():
    """Liderlik tablosunu ekrana yazdırır."""
    leaderboard = load_leaderboard()
    
    print("\n" + "📊 LİDERLİK TABLOSU ".center(50, '='))
    if not leaderboard:
        print("Tablo boş.")
        return
    
    # Sütun başlıkları
    header = f"{'ÖĞRENCİ':<20} {'OKUL':<15} {'PUAN':<10}{'SÜRE':<15}{'TARİH':<20}"
    print(header)
    print("-" * len(header))
    
    for entry in leaderboard[:10]:  # İlk 10'u göster
        score_str = f"{entry['score']}/{entry['total']}"
        school = entry.get('school', 'N/A')[:14]
        print(f"{entry['name'][:19]:<20}{school:<15}{score_str:<10}{entry['duration']:<15}{entry['date']:<20}")
    
    print("="*50 + "\n")

def main_menu():
    """Ana menüyü gösterir ve kullanıcı seçimini işler."""
    word_list = load_words()
    
    while True:
        print("\n" + "🧠 DİLİMİZİN ZENGİNLİKLERİ - MENÜ ".center(50, '-'))
        print(f"Toplam Kelime Sayısı: {len(word_list)}")
        print("1. Oyunu Başlat")
        print("2. Liderlik Tablosu")
        print("3. Çıkış")
        print("-" * 50)
        
        choice = input("Seçiminiz (1/2/3): ").strip()
        
        if choice == '1':
            play_game(word_list)
        elif choice == '2':
            view_leaderboard()
        elif choice == '3':
            print("Güle güle!")
            break
        else:
            print("Geçersiz seçim. Lütfen 1, 2 veya 3 girin.")

if __name__ == "__main__":
    main_menu()