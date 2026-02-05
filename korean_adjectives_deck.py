#!/usr/bin/env python3
"""
Create Anki deck for Korean adjectives with audio.
Front: Korean word
Back: English translation + Korean text + TTS play button
"""

import genanki
import html

# Anki model ID (random unique numbers)
MODEL_ID = 1587991234
DECK_ID = 2087991234

# Define the Anki model with Korean TTS
class KoreanAdjectiveModel(genanki.Model):
    def __init__(self):
        # CSS for styling
        css = """
        .card {
            font-family: 'Arial', sans-serif;
            text-align: center;
            padding: 20px;
        }
        .korean-word {
            font-size: 36px;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .english {
            font-size: 24px;
            color: #555;
            margin-bottom: 15px;
        }
        .korean-back {
            font-size: 28px;
            color: #007bff;
        }
        """

        # Templates
        templates = [
            {
                'name': 'Korean Adjective Card',
                'qfmt': '''
<div class="card">
    <div class="korean-word">{{Korean}}</div>
</div>
''',
                'afmt': '''
<div class="card">
    <div class="english">{{English}}</div>
    <div class="korean-back">{{Korean}}</div>
    <div style="margin-top: 20px;">
        {{FrontSide}}
    </div>
</div>
<script>
// Add Korean TTS button
(function() {
    var button = document.createElement('button');
    button.textContent = '🔊 Play';
    button.style.cssText = 'margin-top: 15px; padding: 10px 20px; font-size: 16px; cursor: pointer; background: #007bff; color: white; border: none; border-radius: 5px;';
    button.onclick = function() {
        var utterance = new SpeechSynthesisUtterance('{{Korean}}');
        utterance.lang = 'ko-KR';
        utterance.rate = 0.8;
        speechSynthesis.speak(utterance);
    };
    var card = document.querySelector('.card');
    if(card) card.appendChild(button);
})();
</script>
''',
            },
        ]

        # Fields
        fields = [
            {'name': 'Korean'},
            {'name': 'English'},
        ]

        super().__init__(
            MODEL_ID,
            'Korean Adjective Model',
            fields=fields,
            templates=templates,
            css=css,
        )


def create_deck():
    """Create the Anki deck with Korean adjectives."""

    # Adjectives data from the website
    adjectives = [
        ("좋다", "good"),
        ("나쁘다", "bad"),
        ("예쁘다", "pretty"),
        ("추워요", "cold (weather)"),
        ("더워요", "hot (weather)"),
        ("크다", "big"),
        ("작다", "small"),
        ("새롭다", "new"),
        ("오래되다", "old (things)"),
        ("멋지다", "cool"),
        ("깨끗하다", "clean"),
        ("더럽다", "dirty"),
        ("높다", "high"),
        ("낮다", "low"),
        ("바쁘다", "busy"),
        ("행복하다", "happy"),
        ("슬프다", "sad"),
        ("신뢰할만하다", "trustworthy"),
        ("불안하다", "anxious"),
        ("진실하다", "truthful"),
        ("건강하다", "healthy"),
        ("아프다", "sick"),
        ("재미있다", "fun"),
        ("지루하다", "boring"),
        ("달콤하다", "sweet"),
        ("쓰다", "bitter"),
        ("무서워요", "scary"),
        ("안전하다", "safe"),
        ("위험하다", "dangerous"),
        ("부자다", "rich"),
        ("가난하다", "poor"),
        ("현명하다", "wise"),
        ("어리다", "young (age)"),
        ("늙다", "old (age)"),
        ("못생기다", "ugly"),
        ("아름답다", "beautiful"),
        ("단순하다", "simple"),
        ("복잡하다", "complex"),
        ("정직하다", "honest"),
        ("부끄럽다", "shy"),
        ("용감하다", "brave"),
        ("소심하다", "timid"),
        ("단조롭다", "monotonous"),
        ("다채롭다", "diverse"),
        ("평범하다", "ordinary"),
        ("특별하다", "special"),
        ("유용하다", "useful"),
        ("무용하다", "useless"),
        ("편안하다", "comfortable"),
        ("불편하다", "uncomfortable"),
        ("기쁘다", "glad"),
        ("불행하다", "unhappy"),
        ("신경쓰이다", "annoying"),
        ("화나다", "angry"),
        ("달다", "sweet (taste)"),
        ("짜다", "salty"),
        ("맵다", "spicy"),
        ("쓰다", "sour"),
        ("신선하다", "fresh"),
        ("상쾌하다", "refreshing"),
        ("살찌다", "fattening"),
        ("다이어트를 위해 좋다", "good for diet"),
        ("충분하다", "sufficient"),
        ("부족하다", "insufficient"),
        ("성실하다", "diligent"),
        ("게으르다", "lazy"),
        ("겸손하다", "humble"),
        ("오만하다", "arrogant"),
        ("명확하다", "clear"),
        ("흐릿하다", "blurry"),
        ("능숙하다", "skilled"),
        ("서투르다", "unskilled"),
        ("답답하다", "frustrating"),
        ("기대하다", "exciting"),
        ("즐겁다", "joyful"),
        ("서운하다", "disappointing"),
        ("만족스럽다", "satisfying"),
        ("실망스럽다", "disheartening"),
        ("궁금하다", "curious"),
        ("확신하다", "confident"),
        ("의심스럽다", "doubtful"),
        ("활발하다", "energetic"),
        ("무관심하다", "indifferent"),
        ("진지하다", "serious"),
        ("경솔하다", "reckless"),
        ("인내심이 있다", "patient"),
        ("선명하다", "clear (vision)"),
        ("희미하다", "dim"),
        ("냄새나다", "smelly"),
        ("냄새 없다", "odorless"),
        ("민감하다", "sensitive"),
        ("둔감하다", "insensitive"),
        ("느리다", "slow"),
        ("빠르다", "fast"),
        ("깊다", "deep"),
        ("얕다", "shallow"),
        ("밝다", "bright"),
        ("어둡다", "dark"),
        ("거칠다", "rough"),
        ("부드럽다", "smooth"),
    ]

    # Create deck
    deck = genanki.Deck(
        DECK_ID,
        'Korean Adjectives - 100 Most Useful'
    )

    # Create model
    model = KoreanAdjectiveModel()

    # Add notes to deck
    for korean, english in adjectives:
        note = genanki.Note(
            model=model,
            fields=[korean, english]
        )
        deck.add_note(note)

    # Save package
    output_file = 'korean_adjectives_100.apkg'
    genanki.Package(deck).write_to_file(output_file)
    print(f"Created Anki deck: {output_file}")
    print(f"Total cards: {len(adjectives)}")
    print("\nImport this file into Anki:")
    print("1. Open Anki")
    print("2. File > Import")
    print(f"3. Select '{output_file}'")


if __name__ == '__main__':
    # Check if genanki is installed
    try:
        import genanki
    except ImportError:
        print("Installing genanki...")
        import subprocess
        subprocess.check_call(['pip', 'install', 'genanki'])
        import genanki

    create_deck()
