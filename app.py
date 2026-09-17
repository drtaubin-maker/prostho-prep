import streamlit as st
import json
import os

# Set page configuration
st.set_page_config(
    page_title="מערכת הכנה למבחן כניסה - שיקום הפה",
    page_icon="🦷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Hebrew RTL & Beautiful UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rubik:wght@300;400;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Rubik', sans-serif;
        direction: rtl;
        text-align: right;
    }
    
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .question-card {
        background-color: #ffffff;
        border: 1px solid #e0e6ed;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    
    .difficulty-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 500;
        font-size: 0.85rem;
        margin-bottom: 10px;
    }
    
    .badge-easy { background-color: #e6f4ea; color: #137333; }
    .badge-medium { background-color: #fef7e0; color: #b06000; }
    .badge-hard { background-color: #feefe3; color: #c5221f; }
    .badge-expert { background-color: #f3e8fd; color: #7627bb; }
    
    .explanation-box {
        background-color: #f8f9fa;
        border-right: 4px solid #1e3c72;
        padding: 1rem 1.2rem;
        margin-top: 1rem;
        border-radius: 4px;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    .stRadio > label {
        font-size: 1.05rem !important;
        font-weight: 500 !important;
    }
</style>
""", unsafe_allow_html=True)

# 15 Topics List
TOPICS = [
    "1. אוקלוזיה, TMJ ותנועות לסת",
    "2. ארטיקולטורים ורישום בין-לסתי",
    "3. עקרונות השחזת שיניים וגאומטריה שיקומית",
    "4. חומרי מטבע וטכניקות הטבעה בשיקום קבוע",
    "5. צמנטים דנטליים, מתכות וסרמיקות",
    "6. תותבות חלקיות נשלפות (RPD): ביומכניקה ומחברים",
    "7. RPD: מאחזים, מסעדים וקומפלקס RPI",
    "8. תותבות שלמות: גבולות אנטומיים ואזורי תמיכה",
    "9. תותבות שלמות: אוקלוזיה, מימד אנכי ויחס בין-לסתי",
    "10. ספיגת עצם אלבאולרית ופתולוגיות רירית",
    "11. שתלים דנטליים: ביומכניקה, איכות עצם ותכנון",
    "12. שיקום על גבי שתלים: מבנים ואפשרויות שיקומיות",
    "13. יחסי גומלין פריודונטיה-שיקום וניידות שיניים",
    "14. תותבות על (Overdentures) ואטצ'מנטים",
    "15. אסתטיקה, בחירת צבע ורפואת שיניים דיגיטלית"
]

# 20 Questions Dataset for Topic 1: Occlusion & TMJ
TOPIC_1_QUESTIONS = [
    # EASY (1-5)
    {
        "id": 1,
        "topic": "1. אוקלוזיה, TMJ ותנועות לסת",
        "difficulty": "קל",
        "question": "מה נכון לגבי המבנה האנטומי של הדיסק הארטיקולרי במפרק הלסת (TMJ)?",
        "options": [
            "א. החלק הקדמי (Anterior band) הוא העבה ביותר בדנטליזציה תקינה.",
            "ב. החלק המרכזי (Intermediate zone) הוא העבה ביותר ומכיל עצבוב עשיר.",
            "ג. החלק האחורי (Posterior band) הוא החלק העבה ביותר בדיסק.",
            "ד. ה-Retrodiscal pad מורכב מסחוס היאליני קשיח ונטול כלי דם."
        ],
        "correct": "ג. החלק האחורי (Posterior band) הוא החלק העבה ביותר בדיסק.",
        "explanation": "לפי שחזורי המבחנים והספרות העיונית (זארב / שילינבורג), הדיסק הארטיקולרי ב-TMJ מורכב מ-Dense connective tissue. החלק האחורי (Posterior band) הוא העבה ביותר, החלק המרכזי (Intermediate zone) הוא הדק ביותר והוא האזור נושא העומס, והחלק הקדמי (Anterior band) בעל עובי בינוני."
    },
    {
        "id": 2,
        "topic": "1. אוקלוזיה, TMJ ותנועות לסת",
        "difficulty": "קל",
        "question": "איזו תכונה מתארת נכונה ארטיקולטור מסוג Arcon בהשוואה לארטיקולטור Non-Arcon?",
        "options": [
            "א. הרכיב הקונדילרי ממוקם בזרוע העליונה והפוסה המכנית ממוקמת בזרוע התחתונה.",
            "ב. הרכיב הקונדילרי ממוקם בזרוע התחתונה והפוסה המכנית ממוקמת בזרוע העליונה, בדומה לאנטומיה האנושית.",
            "ג. שינוי המימד האנכי (VDO) גורם ל-Condylar guidance להשתנות ולהפוך לרדודה יותר.",
            "ד. הוא מתאים לשימוש אך ורק בביצוע תותבות שלמות ולא בשיקומים קבועים."
        ],
        "correct": "ב. הרכיב הקונדילרי ממוקם בזרוע התחתונה והפוסה המכנית ממוקמת בזרוע העליונה, בדומה לאנטומיה האנושית.",
        "explanation": "לפי שילינבורג (פרק 3), בארטיקולטור Arcon הרכיבים הקונדילריים מחוברים לזרוע התחתונה והפוסה לזרוע העליונה (כמו בגולגולת). יתרונו הגדול הוא שבשינוי המימד האנכי (הסרת משנכי שעווה) הזווית בין הפוסה למישור הסגר נשמרת קבועה, ולכן ה-Condylar guidance אינו משתנה."
    },
    {
        "id": 3,
        "topic": "1. אוקלוזיה, TMJ ותנועות לסת",
        "difficulty": "קל",
        "question": "באיזה מדור של מפרק הלסת (TMJ) מתרחשת התנועה הצירית (Rotational / Hinge movement)?",
        "options": [
            "א. במדור העליון (Superior compartment) בלבד.",
            "ב. במדור התחתון (Inferior compartment) בלבד.",
            "ג. בשני המדורים בו-זמנית ובמידה שווה.",
            "ד. בתוך ה-Retrodiscal tissue בלבד."
        ],
        "correct": "ב. במדור התחתון (Inferior compartment) בלבד.",
        "explanation": "התנועה הצירית (תנועת ציר / הרוטציה הראשונית עד פתיחה של כ-20-25 מ\"מ) מתרחשת במדור התחתון של המפרק (בין הקונדיל למשטח התחתון של הדיסק). התנועה המחליקה (Translational movement) מתרחשת במדור העליון (בין הדיסק ל-Articular eminence)."
    },
    {
        "id": 4,
        "topic": "1. אוקלוזיה, TMJ ותנועות לסת",
        "difficulty": "קל",
        "question": "בעת ביצוע צילום פנורמי, התקבלה תמונה בה הלסת התחתונה נראית צרה מדי והעקומה מודגשת. מה קרה במהלך הצילום?",
        "options": [
            "א. המטופל מוקם קדימה מדי (Forward to the focal trough).",
            "ב. המטופל מוקם אחורה מדי (Backward to the focal trough).",
            "ג. ראש המטופל הוטה אחורנית באופן מוגזם.",
            "ד. המטופל נמוך מדי ביחס למכשיר."
        ],
        "correct": "א. המטופל מוקם קדימה מדי (Forward to the focal trough).",
        "explanation": "לפי שחזורי המבחנים והספרות, כאשר המטופל ממוקם קדימה מדי מחוץ ל-Focal trough בצילום פנורמי, השיניים הקדמיות והלסת ייראו מוצרות וצרות (Narrow/magnified in reverse), בעוד שמיקום אחורה מדי גורם להרחבה וטשטוש."
    },
    {
        "id": 5,
        "topic": "1. אוקלוזיה, TMJ ותנועות לסת",
        "difficulty": "קל",
        "question": "איזה שריר מבין הבאים אחראי על התחלת סגירת הלסת (Elevation of the mandible)?",
        "options": [
            "א. Lateral pterygoid",
            "ב. Medial pterygoid",
            "ג. Digastric muscle",
            "ד. Geniohyoid muscle"
        ],
        "correct": "ב. Medial pterygoid",
        "explanation": "לפי השחזורים והספרות העיונית, שריר ה-Medial Pterygoid (יחד עם ה-Masseter וה-Temporalis) הוא מניף הלסת, כאשר בשאלות השחזור מודגש ה-Medial Pterygoid כמי שמתחיל את פעולת ה-Elevation/סגירה."
    },

    # MEDIUM (6-10)
    {
        "id": 6,
        "topic": "1. אוקלוזיה, TMJ ותנועות לסת",
        "difficulty": "בינוני",
        "question": "מהי ההגדרה המדויקת של תנועת Bennett (Bennett Movement / Side Shift)?",
        "options": [
            "א. התנועה הצדית הגופנית (Bodily lateral movement) של הקונדיל בצד העובד (Working side) בעת תנועה לטרלית.",
            "ב. הגלישה הקדמית-מדיאלית של הקונדיל בצד הלא-עובד בלבד.",
            "ג. תנועה אנכית טהורה של המנדיבולה בעת סגירה ב-Centric Relation.",
            "ד. מעבר המנדיבולה מעמדת Rest Position ל-Maximum Intercuspation."
        ],
        "correct": "א. התנועה הצדית הגופנית (Bodily lateral movement) של הקונדיל בצד העובד (Working side) בעת תנועה לטרלית.",
        "explanation": "תנועת Bennett מוגדרת כתנועה הצידית הגופנית של המנדיבולה בצד העובד (Working side condyle). בצד הלא-עובד (Non-working side), תנועה זו משתקפת כזווית Bennett (Bennett angle) והחלקה קדימה, למטה ומדיאלית."
    },
    {
        "id": 7,
        "topic": "1. אוקלוזיה, TMJ ותנועות לסת",
        "difficulty": "בינוני",
        "question": "מה מאפשר לדיסק הארטיקולרי ב-TMJ לנוע קדימה מול ה-Articular Eminence בעת פתיחת פה?",
        "options": [
            "א. היעדר חיבור של הדיסק לעצם הטמפורלית (Lack of direct osseous attachment to the temporal bone).",
            "ב. חיבור גרמי קשיח ל-Tympanic plate.",
            "ג. מתיחה קבועה של ה-Temporomandibular ligament בצד המדיאלי.",
            "ד. הידוק הסיבים האלסטיים התחתונים אל צוואר הקונדיל בלבד."
        ],
        "correct": "א. היעדר חיבור של הדיסק לעצם הטמפורלית (Lack of direct osseous attachment to the temporal bone).",
        "explanation": "לפי ספרי הלימוד (Mohl / Zarb) ושחזורי המבחנים (2016, 2017, 2018), מה שמאפשר לדיסק הארטיקולרי את החופש החלקתי לנוע קדימה יחד עם הקונדיל מול ה-Articular Eminence הוא העובדה שאינו מחובר מורפולוגית ישירות לעצם הטמפורלית."
    },
    {
        "id": 8,
        "topic": "1. אוקלוזיה, TMJ ותנועות לסת",
        "difficulty": "בינוני",
        "question": "לאחר ביצוע רישום בין-לסתי בעובי 4 מ\"מ בארטיקולטור מסוג Non-Arcon והסרת המשנך, הגבסים הובאו למגע אוקלוזלי. מה יתרחש מבחינת ה-Condylar inclination?",
        "options": [
            "א. ה-Condylar inclination תישאר ללא שינוי.",
            "ב. ה-Condylar inclination תשתנה ותהפוך לרדודה יותר (Less steep).",
            "ג. ה-Condylar inclination תשתנה ותהפוך לתלולה יותר (Steeper).",
            "ד. ה-Condylar guidance תתאפס לחלוטין לקו האופק."
        ],
        "correct": "ב. ה-Condylar inclination תשתנה ותהפוך לרדודה יותר (Less steep).",
        "explanation": "לפי שילינבורג (עמ' 28-30), בארטיקולטור Non-Arcon הרכיב הקונדילרי ממוקם בזרוע העליונה. כשסוגרים את המנשך לאחר הסרת משנך בעובי 3-5 מ\"מ, הזווית הגיאומטרית משתנה וההדרכה הקונדילרית הופכת לרדודה יותר (Less steep). בארטיקולטור Arcon היא נשארת ללא שינוי."
    },
    {
        "id": 9,
        "topic": "1. אוקלוזיה, TMJ ותנועות לסת",
        "difficulty": "בינוני",
        "question": "מדוע נקבעת עמדת Centric Relation (CR) כעמדת הייחוס המועדפת בשיקום פה נרחב ובתותבות שלמות?",
        "options": [
            "א. מכיוון שזו עמדה שמוכתבת ע\"י המגעים האוקלוזליים של השיניים הקיימות.",
            "ב. מכיוון שזו עמדה מפרקית אנטומית שניתנת לשחזור (Repeatable/Reproducible) ואינה תלויה במגע שיניים.",
            "ג. מכיוון שבעמדה זו שרירי הלעיסה מגיעים לשיא כוח ההתכווצות שלהם.",
            "ד. מכיוון שבעמדה זו מבוטלת לחלוטין תנועת ה-Bennett side shift."
        ],
        "correct": "ב. מכיוון שזו עמדה מפרקית אנטומית שניתנת לשחזור (Repeatable/Reproducible) ואינה תלויה במגע שיניים.",
        "explanation": "עמדת Centric Relation (CR) מוגדרת כעמדה המפרקית של הקונדילים בחלק הכי אנטרו-סופריורי של הפוסה מול המשטח האוולרי של הדיסק. היא אינה תלויה בשיניים, והיתרון הקליני המרכזי שלה הוא היותה ניתנת לשחזור מדויק ומהווה עמדת מוצא בטוחה לשיקום נרחב."
    },
    {
        "id": 10,
        "topic": "1. אוקלוזיה, TMJ ותנועות לסת",
        "difficulty": "בינוני",
        "question": "למה מתייחס המונח האסתטי \"Gull-Wing Appearance\" במראה המשנן הקדמי העליון?",
        "options": [
            "א. מראה שנוצר עקב שחיקה זוויתית של החותכות המרכזיות.",
            "ב. מצב שבו הקצה האינסיזלי של החותכת הלטרלית העליונה ממוקם אפיקלית לקצוות האינסיזליים של הצנטרלית והניב.",
            "ג. מתאר אנטומי קעור של קו החניכיים מעל הניב בלבד.",
            "ד. מראה שנוצר כאשר קו האמצע הדנטלי מוסט ב-2 מ\"מ מאישוני העיניים."
        ],
        "correct": "ב. מצב שבו הקצה האינסיזלי של החותכת הלטרלית העליונה ממוקם אפיקלית לקצוות האינסיזליים של הצנטרלית והניב.",
        "explanation": "לפי שחזורי המבחנים (2024, 2012), \"Gull-Wing Appearance\" מתאר מתאר אסתטי שבו הקצה האינסיזלי של הלטראלית העליונה קצר יותר (ממוקם אפיקלית) ביחס לקו המחבר את הקצוות האינסיזליים של הצנטרלית והניב, מה שיוצר מראה דמוי כנפי שחף."
    },

    # HARD (11-15)
    {
        "id": 11,
        "topic": "1. אוקלוזיה, TMJ ותנועות לסת",
        "difficulty": "קשה",
        "question": "מה נכון לגבי תופעת ה-Mandibular Flexure בעת הפעלת כוחות סגירה ולעיסה חזקים?",
        "options": [
            "א. התופעה אינהתרחשת במבוגרים עקב הסתיידות של הסימפיזיס.",
            "ב. התופעה מופעלת בעיקר ע\"י התכווצות שרירי ה-Medial Pterygoid, וגורמת להתקרבות ענפי המנדיבולה במישור האופקי.",
            "ג. התופעה גורמת להתרחקות המולרים התחתונים זה מזה בעת פתיחה מקסימלית.",
            "ד. אין לתופעה זו כל השפעה ביומכנית על תכנון שרשראות שתלים או FPD ארוכים."
        ],
        "correct": "ב. התופעה מופעלת בעיקר ע\"י התכווצות שרירי ה-Medial Pterygoid, וגורמת להתקרבות ענפי המנדיבולה במישור האופקי.",
        "explanation": "לפי מיש ושילינבורג ושחזורי המבחנים, בעת פתיחה וסגירה מאומצת שרירי ה-Medial Pterygoid (וה-Lateral Pterygoid) מפעילים כוח הגורם לכפיפה (Mandibular Flexure) של גוף המנדיבולה פנימה (צמצום המרחק הבין-מולרי עד עשרות/מאות מיקרונים). לתופעה זו משמעות קריטית בתכנון גשרים קשיחים וארוכים על שתלים."
    },
    {
        "id": 12,
        "topic": "1. אוקלוזיה, TMJ ותנועות לסת",
        "difficulty": "קשה",
        "question": "למה מיועד רישום ה-Lateral Interocclusal Record (Check bite) בעבודה עם ארטיקולטור חצי-מתכוונן?",
        "options": [
            "א. לקביעת המימד האנכי של הסגר (VDO) בלבד.",
            "ב. למציאת עמדת הקונדילים בפוסה בעת תנועה צדית לקביעת ה-Condylar guidance והגבולות האנטומיים בארטיקולטור.",
            "ג. להעברת יחס הלסת העליונה לבסיס הגולגולת ביחס למישור אורביטלי.",
            "ד. לבדיקת מגעים מטרידים בעמדת Maximum Intercuspation בלבד."
        ],
        "correct": "ב. למציאת עמדת הקונדילים בפוסה בעת תנועה צדית לקביעת ה-Condylar guidance והגבולות האנטומיים בארטיקולטור.",
        "explanation": "לפי הספרות העיונית והשחזורים, רישום Lateral check bite נלקח כדי למקם את הקונדילים בתנועה צדית בפוסה, וכך לכייל את זווית ההדרכה הקונדילרית (Condylar guidance angle) וה-Bennett angle בארטיקולטור חצי-מתכוונן."
    },
    {
        "id": 13,
        "topic": "1. אוקלוזיה, TMJ ותנועות לסת",
        "difficulty": "קשה",
        "question": "מה מבין הבאים אינו נחשב לגורם אטיולוגי להיווצרות סגר כפול (Dual Bite)?",
        "options": [
            "א. תנועה הרגלית פרוטרוזיבית כרונית (כגון Sunday Bite במטופלי Class II div 1).",
            "ב. טיפול אורתודונטי שאינו מלא או בלתי מספק.",
            "ג. סגר אנטומי מסוג Class III קלאסי תורשתי.",
            "ד. מחלה דגנרטיבית של מפרק הלסת (כגון Rheumatoid Arthritis)."
        ],
        "correct": "ג. סגר אנטומי מסוג Class III קלאסי תורשתי.",
        "explanation": "Dual Bite מוגדר כהפרש של מעבר מ-ICP ל-RCP הגדול מ-2 מ\"מ (קיים ב-1-3% באוכלוסיה). הגורמים המוכרים בספרות (Egermack-Eriksson / שחזורי 2018-2020): תנועה הרגלית פרוטרוזיבית (Sunday bite), טיפול אורתו לא מלא, שבר דו-צדדי במפרק, ומחלות דגנרטיביות. Class III אנטומי אינו גורם ל-Dual bite."
    },
    {
        "id": 14,
        "topic": "1. אוקלוזיה, TMJ ותנועות לסת",
        "difficulty": "קשה",
        "question": "במטופל עם סגר Class 2 שבו בוצעה הרמת מנשך (הגדלת VDO), המשנן התחתון זז דיסטלית ביחס לעליון. מה עלינו לעשות כדי לשחזר מגעים קדמיים ב-MI?",
        "options": [
            "א. להאריך את החותכות התחתונות בלבד.",
            "ב. להוסיף למתאר הפלטינלי של הקדמיות העליונות ולייצר פלטפורמה (Palatal Platform).",
            "ג. להוריד לחלוטין את התלוליות הבוקאליות במלוא המשנן התחתון.",
            "ד. להטות את החותכות התחתונות לינגואלית ב-15 מעלות."
        ],
        "correct": "ב. להוסיף למתאר הפלטינלי של הקדמיות העליונות ולייצר פלטפורמה (Palatal Platform).",
        "explanation": "לפי שחזורי המבחנים (2024, 2012), כאשר מגדילים מימד אנכי במטופל Class 2, הקונדילים מסתובבים והמנדיבולה נעה אחורנית (דיסטלית) ביחס למקסילה. כדי ליצור מגעים קדמיים ב-MI יש להוסיף נפח למתאר הפלטינלי של הקדמיות העליונות (Building a palatal ledge/platform)."
    },
    {
        "id": 15,
        "topic": "1. אוקלוזיה, TMJ ותנועות לסת",
        "difficulty": "קשה",
        "question": "מה נכון לגבי המרחק הבין-קונדילרי (Intercondylar distance) בארטיקולטורים סמי-אדג'סטבל סטנדרטיים?",
        "options": [
            "א. הוא נקבע ל-90 מ\"מ קבוע מראש בכל הדגמים.",
            "ב. בארטיקולטורים ממוצעים המרחק נקבע לכ-110 מ\"מ (בעוד שבגולגולת האדם הוא משתנה בין אינדיבידואלים).",
            "ג. הוא קובע באופן ישיר את עקומת Spee במקביל לקשת הפנים.",
            "ד. ככל שהמרחק הבין-קונדילרי קטן יותר, הזווית בין שבילי הגלישה הבוקאליים והלינגואליים גדלה."
        ],
        "correct": "ב. בארטיקולטורים ממוצעים המרחק נקבע לכ-110 מ\"מ (בעוד שבגולגולת האדם הוא משתנה בין אינדיבידואלים).",
        "explanation": "לפי הספרות (שילינבורג / מול) ושחזורי המבחנים (2016–2024), המרחק הבין-קונדילרי הממוצע בארטיקולטורים חצי-מתכווננים הוא 110 מ\"מ. באדם המרחק הוא אינדיבידואלי ומשתנה."
    },

    # EXPERT (16-20)
    {
        "id": 16,
        "topic": "1. אוקלוזיה, TMJ ותנועות לסת",
        "difficulty": "מומחה",
        "question": "על פי הספרות העיונית (שילינבורג / מול) והשחזורים, ממה נובעת תחילת התנועה הצדית בצד העובד (Working Side) לעומת הצד הלא-עובד (Non-Working Side)?",
        "options": [
            "א. התחלת התנועה בצד העובד נובעת מהשפעת ה-Temporomandibular Ligament, ובצד הלא-עובד מהקיר המדיאלי של ה-Glenoid Fossa.",
            "ב. התחלת התנועה בצד העובד מוכתבת אך ורק ע\"י התכווצות שריר ה-Masseter בצד הנגדי.",
            "ג. הקיר הלטרלי של ה-Glenoid fossa בצד העובד הוא הגורם היחיד המכתיב את ה-Progressive side shift.",
            "ד. הדיסק הארטיקולרי ננעל לחלוטין בצד הלא-עובד ומונע גלישה מדיאלית."
        ],
        "correct": "א. התחלת התנועה בצד העובד נובעת מהשפעת ה-Temporomandibular Ligament, ובצד הלא-עובד מהקיר המדיאלי של ה-Glenoid Fossa.",
        "explanation": "לפי שחזורי המבחנים (2018, 2019) וציטוטי הלימוד מהספרות, תחילת תנועת ה-Side shift בצד העובד מושפעת ומרוסנת ע\"י ה-Temporomandibular ligament בצד העובד, ובצד הלא-עובד היא מותנית במבנה הקיר המדיאלי של ה-Glenoid fossa."
    },
    {
        "id": 17,
        "topic": "1. אוקלוזיה, TMJ ותנועות לסת",
        "difficulty": "מומחה",
        "question": "מהו ההבדל המדויק בין המושגים Condylar Angulation לבין Condylar Inclination בספרות הדנטלית ושחזורי המבחנים?",
        "options": [
            "א. הראשון (Condylar Angulation) נמדד בצד הלא-עובד במישור הוריזונטלי (מקורו בתנועת Bennett), והשני (Condylar Inclination) נמדד בפרוטרוזיה במישור פרה-סגיטלי.",
            "ב. הראשון נמדד בתנועה פונקציונלית של סגירה בלבד, והשני נמדד בעת מנוחה (VDR).",
            "ג. הראשון מוגדר רק בארטיקולטור Non-Arcon והשני מוגדר רק בארטיקולטור Arcon.",
            "ד. אין שום הבדל ביניהם – מדובר בשמות נרדפים לאותה זווית הדרכה."
        ],
        "correct": "א. הראשון (Condylar Angulation) נמדד בצד הלא-עובד במישור הוריזונטלי (מקורו בתנועת Bennett), והשני (Condylar Inclination) נמדד בפרוטרוזיה במישור פרה-סגיטלי.",
        "explanation": "לפי שחזורי המבחנים (2016-2019): Condylar Angulation מקורו בתנועת Bennett ונמדד בצד הלא עובד במישור הוריזונטלי (או זווית Bennett), בעוד Condylar Inclination נמדד בעת גלישה קדימה (פרוטרוזיה) במישור פרה-סגיטלי (זווית ההדרכה הקונדילרית)."
    },
    {
        "id": 18,
        "topic": "1. אוקלוזיה, TMJ ותנועות לסת",
        "difficulty": "מומחה",
        "question": "מהי המשמעות הביומכנית המלאה של סגר מוגן הדדית (Mutually Protected Occlusion / Organic Occlusion)?",
        "options": [
            "א. השיניים האחוריות מגינות על הקדמיות בעמדת MI (סופגות את הכוחות המאונכים), והשיניים הקדמיות מפרידות (Disclude) את האחוריות בתנועות אקסצנטריות.",
            "ב. השיניים הקדמיות והאחוריות עומדות במגע הדוק והרמוני בכל תנועות הגלישה הלטרליות והפרוטרוזיביות.",
            "ג. הניבים בלבד נושאים בכל עומס הסגירה ב-MI ללא מגע בטוחנות.",
            "ד. מגע רציף של כל התלוליות בצד העובד והלא-עובד בעת ובעונה אחת."
        ],
        "correct": "א. השיניים האחוריות מגינות על הקדמיות בעמדת MI (סופגות את הכוחות המאונכים), והשיניים הקדמיות מפרידות (Disclude) את האחוריות בתנועות אקסצנטריות.",
        "explanation": "סגר מוגן הדדית (Mutually Protected Occlusion) מתבסס על כך שבסגירה מרכזית (MI) השיניים האחוריות סופגות את העומס האנכי ומגינות על הקדמיות (מגע קל/מרפרף בקדמיות), ואילו בגלישה אקסצנטרית (לטרלית/פרוטרוזיה) השיניים הקדמיות/ניבים מנחות ומפרידות (Disclude) את האחוריות."
    },
    {
        "id": 19,
        "topic": "1. אוקלוזיה, TMJ ותנועות לסת",
        "difficulty": "מומחה",
        "question": "משוואת Hanau (Hanau's Quint) מגדירה 5 פרמטרים ליצירת Balanced Occlusion. איזה מהגורמים הבאים נמצא בשליטתו הישירה של רופא השיניים בתכנון המשנן?",
        "options": [
            "א. Condylar Guidance (זווית ההדרכה הקונדילרית במפרק).",
            "ב. Incisal Guidance, Cusp Height, ו-Plane of Occlusion / Curve of Spee.",
            "ג. האנטומיה הגרמית של ה-Glenoid Fossa.",
            "ד. קצב ספיגת העצם האלבאולרית ברכס השארי."
        ],
        "correct": "ב. Incisal Guidance, Cusp Height, ו-Plane of Occlusion / Curve of Spee.",
        "explanation": "במשוואת Hanau (המחברת בין Condylar Guidance, Incisal Guidance, Cusp Height, Plane of Occlusion, ו-Curve of Spee/Compensation), ה-Condylar Guidance נקבעת ע\"י אנטומיית המטופל ואינה נשלטת ע\"י הרופא. לעומת זאת, גובה התלוליות, ההדרכה האינסיזלית, ומישור הסגר/עקומות הפיצוי נשלטים ע\"י הקלינאי."
    },
    {
        "id": 20,
        "topic": "1. אוקלוזיה, TMJ ותנועות לסת",
        "difficulty": "מומחה",
        "question": "מה יתרחש ברירית החך/הרכס (Mucosa) תחת עומס לחיצה מודרני מתמיד של 10 דקות במטופל מבוגר (Viscoelastic behavior)?",
        "options": [
            "א. בהתחלה דחיסה אלסטית מהירה ולאחר מכן דפורמציה אלסטית איטית, כאשר החזרה למימדים המקוריים עשויה להימשך עד 4 שעות.",
            "ב. דפורמציה פלסטית בלתי הפיכה באופן מיידי.",
            "ג. דחיסה פלסטית מהירה בשתי הדקות הראשונות בלבד ולאחריה עצירה מוחלטת.",
            "ד. הרחבה אלסטית מיידית של הרקמה התת-רירית ללא השפעת זמן."
        ],
        "correct": "א. בהתחלה דחיסה אלסטית מהירה ולאחר מכן דפורמציה אלסטית איטית, כאשר החזרה למימדים המקוריים עשויה להימשך עד 4 שעות.",
        "explanation": "לפי Boucher ושחזורי המבחנים (2016), ההתנהגות הוויסקואלסטית של הרקמה הרכה תחת עומס של 10 דקות כוללת התכווצות אלסטית מהירה בהתחלה ודפורמציה איטית בהמשך. החזרה המלאה למימדים המקוריים במטופלים מבוגרים עשויה להימשך עד 4 שעות."
    }
]

# Simple Data persistence file
DATA_FILE = "user_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {"users": {}}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Initialize Session State
if "user_data" not in st.session_state:
    st.session_state.user_data = load_data()

# Header
st.markdown("""
<div class="main-header">
    <h1>🦷 מדרשת שיקום הפה - אתר הלמידה והתרגול</h1>
    <p>הכנה ממוקדת למבחן הכניסה בהתמחות בשיקום הפה | מבוסס ספרות ושחזורים</p>
</div>
""", unsafe_allow_html=True)

# Sidebar - User Profile & Navigation
st.sidebar.header("👤 פרופיל משתמש")
current_user = st.sidebar.selectbox(
    "בחר/י שם מתמחה:",
    ["ד\"ר דורון", "ד\"ר עפרה", "ד\"ר יארה"]
)

st.sidebar.markdown("---")
st.sidebar.header("📚 ניווט וסינון")

selected_topic = st.sidebar.selectbox(
    "בחר נושא לימוד (מתוך 15):",
    TOPICS
)

selected_difficulty = st.sidebar.radio(
    "רמת קושי:",
    ["הכל (20 שאלות)", "קל", "בינוני", "קשה", "מומחה"]
)

# Ensure user entry exists in state
if current_user not in st.session_state.user_data["users"]:
    st.session_state.user_data["users"][current_user] = {
        "answers": {},
        "ratings": {},
        "feedback": {}
    }

user_profile = st.session_state.user_data["users"][current_user]

# Content Area
st.subheader(f"📌 {selected_topic}")

if selected_topic.startswith("1."):
    # Filter questions for Topic 1
    if selected_difficulty == "הכל (20 שאלות)":
        filtered_q = TOPIC_1_QUESTIONS
    else:
        filtered_q = [q for q in TOPIC_1_QUESTIONS if q["difficulty"] == selected_difficulty]
        
    st.info(f"מציג **{len(filtered_q)}** שאלות ברמת קושי: **{selected_difficulty}** עבור **{current_user}**")
    
    score = 0
    total_answered = 0
    
    for idx, q in enumerate(filtered_q, 1):
        q_id = str(q["id"])
        
        # Difficulty Badge Style
        badge_class = {
            "קל": "badge-easy",
            "בינוני": "badge-medium",
            "קשה": "badge-hard",
            "מומחה": "badge-expert"
        }.get(q["difficulty"], "badge-easy")
        
        st.markdown(f"""
        <div class="question-card">
            <span class="difficulty-badge {badge_class}">דרגה: {q["difficulty"]}</span>
            <h3>שאלה {idx}: {q["question"]}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # User Answer Selection
        saved_answer = user_profile["answers"].get(q_id, None)
        
        selected_opt = st.radio(
            f"בחר/י תשובה לשאלה {idx}:",
            q["options"],
            index=q["options"].index(saved_answer) if saved_answer in q["options"] else None,
            key=f"q_{q_id}_{current_user}"
        )
        
        if selected_opt:
            user_profile["answers"][q_id] = selected_opt
            total_answered += 1
            
            if selected_opt == q["correct"]:
                st.success("✅ תשובה נכונה!")
                score += 1
            else:
                st.error(f"❌ תשובה שגויה. התשובה הנכונה היא: **{q['correct']}**")
            
            # Explanation
            st.markdown(f"""
            <div class="explanation-box">
                <strong>💡 הסבר מפורט מהספרות והשחזורים:</strong><br>
                {q['explanation']}
            </div>
            """, unsafe_allow_html=True)
            
            # Question Quality Rating (1-5)
            st.markdown("---")
            col1, col2 = st.columns([1, 2])
            with col1:
                saved_rating = user_profile["ratings"].get(q_id, 5)
                rating = st.slider(
                    "דירוג איכות השאלה והמסיחים (1-5):",
                    1, 5, value=saved_rating, key=f"rate_{q_id}_{current_user}"
                )
                user_profile["ratings"][q_id] = rating
            
            with col2:
                saved_fb = user_profile["feedback"].get(q_id, "")
                fb_text = st.text_input(
                    "הערה/משוב אישי לשאלה זו (אופציונלי):",
                    value=saved_fb, key=f"fb_{q_id}_{current_user}"
                )
                user_profile["feedback"][q_id] = fb_text
                
        st.markdown("<br>", unsafe_allow_html=True)

    # Save state
    save_data(st.session_state.user_data)
    
    # Progress Summary
    if total_answered > 0:
        st.sidebar.markdown("---")
        st.sidebar.subheader("📊 סיכום התקדמות אישית")
        st.sidebar.progress(total_answered / len(filtered_q))
        st.sidebar.write(f"ענית על **{total_answered}** מתוך **{len(filtered_q)}** שאלות")
        st.sidebar.write(f"ציון נוכחי: **{int((score/total_answered)*100)}%** ({score}/{total_answered})")

else:
    st.warning("⚠️ הקפסולה עבור נושא זה נמצאת בשלבי בנייה ותועלה בקרוב! כרגע ניתן לתרגל את נושא 1 (אוקלוזיה, TMJ ותנועות לסת).")
