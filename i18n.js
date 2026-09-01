/**
 * SchemeSaathi - 15 Indian Languages Native Multilingual Engine & Full DOM Auto-Translator
 * Zero external dependencies. High-performance bidirectional string preservation engine.
 */

(function(window) {
  'use strict';

  const PHRASE_MAPS = {
  "en": {
    "SchemeSaathi": "SchemeSaathi",
    "Citizen Government Scheme Action Platform": "Citizen Government Scheme Action Platform",
    "Verified .gov.in Registry": "Verified .gov.in Registry",
    "I Need Help (Grievance Desk)": "I Need Help (Grievance Desk)",
    "Official Security Notice:": "Official Security Notice:",
    "SchemeSaathi will NEVER ask for your government portal passwords, OTP, or UPI PIN. Beware of unofficial agents.": "SchemeSaathi will NEVER ask for your government portal passwords, OTP, or UPI PIN. Beware of unofficial agents.",
    "All Government Schemes": "All Government Schemes",
    "For Me (Eligible)": "For Me (Eligible)",
    "My Documents": "My Documents",
    "My Applications": "My Applications",
    "Comparison": "Comparison",
    "Life-Events": "Life-Events",
    "Fraud Shield": "Fraud Shield",
    "My Privacy": "My Privacy",
    "Admin Registry": "Admin Registry",
    "MY BENEFITS HEALTH CHECK": "MY BENEFITS HEALTH CHECK",
    "Live health status based on your profile and document readiness": "Live health status based on your profile and document readiness",
    "Eligible Schemes": "Eligible Schemes",
    "High Priority": "High Priority",
    "Ready to Apply": "Ready to Apply",
    "Applications In Progress": "Applications In Progress",
    "Missing Documents": "Missing Documents",
    "Expiring Documents": "Expiring Documents",
    "Upcoming Deadlines": "Upcoming Deadlines",
    "MY NEXT ACTION": "MY NEXT ACTION",
    "Step 1: Gather Required Documents": "Step 1: Gather Required Documents",
    "Apply on Official Portal": "Apply on Official Portal",
    "RECOMMENDED": "RECOMMENDED",
    "APPLICATION READINESS": "APPLICATION READINESS",
    "View Details": "View Details",
    "Readiness Score": "Readiness Score",
    "Apply on .gov.in": "Apply on .gov.in",
    "Compare": "Compare",
    "Why Recommended for You": "Why Recommended for You",
    "Document Gap Analysis": "Document Gap Analysis",
    "Missing": "Missing",
    "Filter by": "Filter by",
    "All Categories": "All Categories",
    "Matching Schemes": "Matching Schemes",
    "Search matching schemes...": "Search matching schemes...",
    "All Government Schemes Catalogue": "All Government Schemes Catalogue",
    "Search by scheme name, keyword, category, ministry, or benefit...": "Search by scheme name, keyword, category, ministry, or benefit...",
    "Close": "Close",
    "Save Profile & Recalculate Schemes": "Save Profile & Recalculate Schemes",
    "Report Missing Scheme": "Report Missing Scheme"
  },
  "hi": {
    "SchemeSaathi": "स्कीम साथी",
    "Citizen Government Scheme Action Platform": "नागरिक सरकारी योजना कार्य मंच",
    "Verified .gov.in Registry": "सत्यापित .gov.in रजिस्ट्री",
    "I Need Help (Grievance Desk)": "मुझे मदद चाहिए (शिकायत निवारण)",
    "Official Security Notice:": "आधिकारिक सुरक्षा सूचना:",
    "SchemeSaathi will NEVER ask for your government portal passwords, OTP, or UPI PIN. Beware of unofficial agents.": "स्कीम साथी आपसे कभी भी सरकारी पोर्टल पासवर्ड, ओटीपी या यूपीआई पिन नहीं मांगेगा। अनाधिकृत एजेंटों से सावधान रहें।",
    "All Government Schemes": "सभी सरकारी योजनाएं",
    "For Me (Eligible)": "मेरे लिए (पात्र)",
    "My Documents": "मेरे दस्तावेज़",
    "My Applications": "मेरे आवेदन",
    "Comparison": "तुलना करें",
    "Life-Events": "जीवन-घटनाएं",
    "Fraud Shield": "धोखाधड़ी सुरक्षा",
    "My Privacy": "मेरी गोपनीयता",
    "Admin Registry": "व्यवस्थापक रजिस्ट्री",
    "MY BENEFITS HEALTH CHECK": "मेरी योजना स्वास्थ्य जांच",
    "Live health status based on your profile and document readiness": "आपकी प्रोफ़ाइल और दस्तावेज़ तत्परता के आधार पर वास्तविक स्वास्थ्य स्थिति",
    "Eligible Schemes": "पात्र योजनाएं",
    "High Priority": "उच्च प्राथमिकता",
    "Ready to Apply": "आवेदन के लिए तैयार",
    "Applications In Progress": "प्रक्रियाधीन आवेदन",
    "Missing Documents": "अनुपलब्ध दस्तावेज़",
    "Expiring Documents": "समाप्त होने वाले दस्तावेज़",
    "Upcoming Deadlines": "आगामी अंतिम तिथियां",
    "MY NEXT ACTION": "मेरा अगला कदम",
    "Step 1: Gather Required Documents": "कदम 1: आवश्यक दस्तावेज़ एकत्र करें",
    "Apply on Official Portal": "आधिकारिक पोर्टल पर आवेदन करें",
    "RECOMMENDED": "अनुशंसित",
    "APPLICATION READINESS": "आवेदन तत्परता",
    "View Details": "विवरण देखें",
    "Readiness Score": "तत्परता स्कोर",
    "Apply on .gov.in": ".gov.in पर आवेदन करें",
    "Compare": "तुलना करें",
    "Why Recommended for You": "आपके लिए अनुशंसित क्यों",
    "Document Gap Analysis": "दस्तावेज़ अंतर विश्लेषण",
    "Missing": "अनुपलब्ध",
    "Filter by": "फ़िल्टर करें",
    "All Categories": "सभी श्रेणियां",
    "Matching Schemes": "मिलान योजनाएं",
    "Search matching schemes...": "पात्र योजनाएं खोजें...",
    "All Government Schemes Catalogue": "सभी सरकारी योजनाओं की सूची",
    "Search by scheme name, keyword, category, ministry, or benefit...": "योजना का नाम, कीवर्ड, श्रेणी, मंत्रालय या लाभ से खोजें...",
    "Close": "बंद करें",
    "Save Profile & Recalculate Schemes": "प्रोफ़ाइल सहेजें और योजनाएं पुनर्गणना करें",
    "Report Missing Scheme": "अनुपलब्ध योजना की रिपोर्ट करें"
  },
  "mr": {
    "SchemeSaathi": "स्कीम साथी",
    "Citizen Government Scheme Action Platform": "नागरिक सरकारी योजना कृती मंच",
    "Verified .gov.in Registry": "सत्यापित .gov.in नोंदवही",
    "I Need Help (Grievance Desk)": "मला मदत हवी आहे (तक्रार निवारण)",
    "Official Security Notice:": "अधिकृत सुरक्षा सूचना:",
    "SchemeSaathi will NEVER ask for your government portal passwords, OTP, or UPI PIN. Beware of unofficial agents.": "स्कीम साथी आपल्याकडून कधीही सरकारी पासवर्ड, OTP किंवा UPI PIN मागणार नाही. अनधिकृत व्यक्तींपासून सावध राहा.",
    "All Government Schemes": "सर्व सरकारी योजना",
    "For Me (Eligible)": "माझ्यासाठी (पात्र)",
    "My Documents": "माझे दस्तऐवज",
    "My Applications": "माझे अर्ज",
    "Comparison": "तुलना करा",
    "Life-Events": "जीवन-घटना",
    "Fraud Shield": "सुरक्षा कवच",
    "My Privacy": "माझी गोपनीयता",
    "Admin Registry": "प्रशासक नोंदवही",
    "MY BENEFITS HEALTH CHECK": "माझी योजना आरोग्य तपासणी",
    "Live health status based on your profile and document readiness": "तुमच्या प्रोफाइल आणि दस्तऐवज तयारीवर आधारित थेट आरोग्य स्थिती",
    "Eligible Schemes": "पात्र योजना",
    "High Priority": "उच्च प्राधान्य",
    "Ready to Apply": "अर्जासाठी सज्ज",
    "Applications In Progress": "प्रक्रियेतील अर्ज",
    "Missing Documents": "अपूर्ण दस्तऐवज",
    "Expiring Documents": "कालबाह्य होणारे दस्तऐवज",
    "Upcoming Deadlines": "आगामी अंतिम मुदती",
    "MY NEXT ACTION": "माझी पुढील कृती",
    "Step 1: Gather Required Documents": "टप्पा १: आवश्यक दस्तऐवज गोळा करा",
    "Apply on Official Portal": "अधिकृत पोर्टलवर अर्ज करा",
    "RECOMMENDED": "शिफारस केलेली",
    "APPLICATION READINESS": "अर्ज तयारी",
    "View Details": "तपशील पहा",
    "Readiness Score": "तयारी गुण",
    "Apply on .gov.in": ".gov.in वर अर्ज करा",
    "Compare": "तुलना करा",
    "Why Recommended for You": "तुमच्यासाठी शिफारस का",
    "Document Gap Analysis": "दस्तऐवज पडताळणी विश्लेषण",
    "Missing": "अपूर्ण",
    "Filter by": "फिल्टर करा",
    "All Categories": "सर्व श्रेणी",
    "Matching Schemes": "पात्र योजना",
    "Search matching schemes...": "योजना शोधा...",
    "All Government Schemes Catalogue": "सर्व सरकारी योजना सूची",
    "Search by scheme name, keyword, category, ministry, or benefit...": "योजनेचे नाव, कीवर्ड, श्रेणी, मंत्रालय किंवा लाभाने शोधा...",
    "Close": "बंद करा",
    "Save Profile & Recalculate Schemes": "प्रोफाइल जतन करा आणि योजना पुन्हा तपासा",
    "Report Missing Scheme": "सुटलेली योजना नोंदवा"
  },
  "bn": {
    "SchemeSaathi": "স্কিম সাথী",
    "Citizen Government Scheme Action Platform": "নাগরিক সরকারি স্কিম প্ল্যাটফর্ম",
    "Verified .gov.in Registry": "যাচাইকৃত .gov.in রেজিস্ট্রি",
    "I Need Help (Grievance Desk)": "সাহায্য প্রয়োজন (অভিযোগ ডেস্ক)",
    "Official Security Notice:": "অফিসিয়াল নিরাপত্তা বিজ্ঞপ্তি:",
    "SchemeSaathi will NEVER ask for your government portal passwords, OTP, or UPI PIN. Beware of unofficial agents.": "স্কিম সাথী কখনোই আপনার সরকারি পাসওয়ার্ড, ওটিপি বা ইউপিআই পিন চাইবে না।",
    "All Government Schemes": "সকল সরকারি স্কিম",
    "For Me (Eligible)": "আমার জন্য (যোগ্য)",
    "My Documents": "আমার নথিপত্র",
    "My Applications": "আমার আবেদনসমূহ",
    "Comparison": "তুলনা",
    "Life-Events": "জীবন-ঘটনা",
    "Fraud Shield": "প্রতারণা সুরক্ষা",
    "My Privacy": "আমার গোপনীয়তা",
    "Admin Registry": "অ্যাডমিন রেজিস্ট্রি",
    "MY BENEFITS HEALTH CHECK": "আমার স্কিম স্বাস্থ্য পরীক্ষা",
    "Live health status based on your profile and document readiness": "আপনার প্রোফাইল এবং নথির প্রস্তুতির উপর ভিত্তি করে স্বাস্থ্য স্থিতি",
    "Eligible Schemes": "যোগ্য স্কিমসমূহ",
    "High Priority": "উচ্চ অগ্রাধিকার",
    "Ready to Apply": "আবেদনের জন্য প্রস্তুত",
    "Applications In Progress": "চলমান আবেদনসমূহ",
    "Missing Documents": "অনুপস্থিত নথিপত্র",
    "Expiring Documents": "মেয়াদোত্তীর্ণ নথিপত্র",
    "Upcoming Deadlines": "আসন্ন শেষ তারিখসমূহ",
    "MY NEXT ACTION": "আমার পরবর্তী পদক্ষেপ",
    "Step 1: Gather Required Documents": "পদক্ষেপ ১: প্রয়োজনীয় নথিপত্র সংগ্রহ করুন",
    "Apply on Official Portal": "অফিসিয়াল পোর্টালে আবেদন করুন",
    "RECOMMENDED": "প্রস্তাবিত",
    "APPLICATION READINESS": "আবেদন প্রস্তুতি",
    "View Details": "বিস্তারিত দেখুন",
    "Readiness Score": "প্রস্তুতি স্কোর",
    "Apply on .gov.in": ".gov.in-এ আবেদন করুন",
    "Compare": "তুলনা",
    "Why Recommended for You": "আপনার জন্য কেন প্রস্তাবিত",
    "Document Gap Analysis": "নথি ঘাটতি বিশ্লেষণ",
    "Missing": "অনুপস্থিত",
    "Filter by": "ফিল্টার করুন",
    "All Categories": "সকল বিভাগ",
    "Matching Schemes": "উপযুক্ত স্কিমসমূহ",
    "Search matching schemes...": "স্কিম খুঁজুন...",
    "All Government Schemes Catalogue": "সকল সরকারি স্কিমের তালিকা",
    "Search by scheme name, keyword, category, ministry, or benefit...": "স্কিমের নাম, কীওয়ার্ড, বিভাগ বা মন্ত্রণালয় দিয়ে অনুসন্ধান করুন...",
    "Close": "বন্ধ করুন",
    "Save Profile & Recalculate Schemes": "প্রোফাইল সংরক্ষণ করুন ও স্কিম পুনঃগণনা করুন",
    "Report Missing Scheme": "অনুপস্থিত স্কিম রিপোর্ট করুন"
  },
  "gu": {
    "SchemeSaathi": "સ્કીમ સાથી",
    "Citizen Government Scheme Action Platform": "નાગરિક સરકારી યોજના પ્લેટફોર્મ",
    "Verified .gov.in Registry": "ચકાસાયેલ .gov.in રજિસ્ટ્રી",
    "I Need Help (Grievance Desk)": "મને મદદ જોઈએ છે (ફરિયાદ ડેસ્ક)",
    "Official Security Notice:": "સત્તાવાર સુરક્ષા સૂચના:",
    "SchemeSaathi will NEVER ask for your government portal passwords, OTP, or UPI PIN. Beware of unofficial agents.": "સ્કીમ સાથી ક્યારેય તમારા સરકારી પાસવર્ડ, ઓટીપી કે યુપીઆઈ પિન માંગશે નહીં.",
    "All Government Schemes": "બધી સરકારી યોજનાઓ",
    "For Me (Eligible)": "મારા માટે (પાત્ર)",
    "My Documents": "મારા દસ્તાવેજો",
    "My Applications": "મારી અરજીઓ",
    "Comparison": "તુલના",
    "Life-Events": "જીવન-ઘટનાઓ",
    "Fraud Shield": "છેતરપિંડી સુરક્ષા",
    "My Privacy": "મારી ગોપનીયતા",
    "Admin Registry": "એડમિન રજિસ્ટ્રી",
    "MY BENEFITS HEALTH CHECK": "મારી યોજના આરોગ્ય તપાસ",
    "Live health status based on your profile and document readiness": "તમારી પ્રોફાઇલ અને દસ્તાવેજ સજ્જતા પર આધારિત સ્થિતિ",
    "Eligible Schemes": "પાત્ર યોજનાઓ",
    "High Priority": "ઉચ્ચ પ્રાથમિકતા",
    "Ready to Apply": "અરજી કરવા માટે તૈયાર",
    "Applications In Progress": "પ્રક્રિયા હેઠળની અરજીઓ",
    "Missing Documents": "ખૂટતા દસ્તાવેજો",
    "Expiring Documents": "મુદ્દત વીતી ગયેલા દસ્તાવેજો",
    "Upcoming Deadlines": "આગામી અંતિમ તારીખો",
    "MY NEXT ACTION": "મારું આગલું પગલું",
    "Step 1: Gather Required Documents": "પગલું ૧: જરૂરી દસ્તાવેજો એકત્રિત કરો",
    "Apply on Official Portal": "સત્તાવાર પોર્ટલ પર અરજી કરો",
    "RECOMMENDED": "ભલામણ કરેલ",
    "APPLICATION READINESS": "અરજી સજ્જતા",
    "View Details": "વિગતો જુઓ",
    "Readiness Score": "સજ્જતા સ્કોર",
    "Apply on .gov.in": ".gov.in પર અરજી કરો",
    "Compare": "તુલના",
    "Why Recommended for You": "તમારા માટે શા માટે ભલામણ કરેલ",
    "Document Gap Analysis": "દસ્તાવેજ અંતર વિશ્લેષણ",
    "Missing": "ખૂટે છે",
    "Filter by": "ફિલ્ટર કરો",
    "All Categories": "બધી શ્રેણીઓ",
    "Matching Schemes": "મેળ ખાતી યોજનાઓ",
    "Search matching schemes...": "યોજનાઓ શોધો...",
    "All Government Schemes Catalogue": "બધી સરકારી યોજનાઓની સૂચિ",
    "Search by scheme name, keyword, category, ministry, or benefit...": "યોજનાનું નામ, કીવર્ડ, શ્રેણી અથવા મંત્રાલય દ્વારા શોધો...",
    "Close": "બંધ કરો",
    "Save Profile & Recalculate Schemes": "પ્રોફાઇલ સાચવો અને યોજનાઓ ફરી ગણો",
    "Report Missing Scheme": "ખૂટતી યોજનાની જાણ કરો"
  },
  "ta": {
    "SchemeSaathi": "ஸ்கீம் சாதி",
    "Citizen Government Scheme Action Platform": "குடிமக்கள் அரசுத் திட்ட தளம்",
    "Verified .gov.in Registry": "சரிபார்க்கப்பட்ட .gov.in பதிவேடு",
    "I Need Help (Grievance Desk)": "உதவி தேவை (குறைதீர்ப்பு)",
    "Official Security Notice:": "அதிகாரப்பூர்வ பாதுகாப்பு அறிவிப்பு:",
    "SchemeSaathi will NEVER ask for your government portal passwords, OTP, or UPI PIN. Beware of unofficial agents.": "ஸ்கீம் சாதி ஒருபோதும் கடவுச்சொல், OTP அல்லது UPI PIN கேட்காது.",
    "All Government Schemes": "அனைத்து அரசுத் திட்டங்கள்",
    "For Me (Eligible)": "எனக்கானவை (தகுதியானவை)",
    "My Documents": "எனது ஆவணங்கள்",
    "My Applications": "எனது விண்ணப்பங்கள்",
    "Comparison": "ஒப்பீடு",
    "Life-Events": "வாழ்க்கை நிகழ்வுகள்",
    "Fraud Shield": "மோசடி தடுப்பு",
    "My Privacy": "எனது தனியுரிமை",
    "Admin Registry": "நிர்வாகப் பதிவேடு",
    "MY BENEFITS HEALTH CHECK": "எனது திட்ட சுகாதார சோதனை",
    "Live health status based on your profile and document readiness": "உங்கள் சுயவிவரம் மற்றும் ஆவணத் தயார்நிலை அடிப்படையிலான நிலை",
    "Eligible Schemes": "தகுதியான திட்டங்கள்",
    "High Priority": "உயர் முன்னுரிமை",
    "Ready to Apply": "விண்ணப்பிக்க தயார்",
    "Applications In Progress": "செயல்பாட்டில் உள்ள விண்ணப்பங்கள்",
    "Missing Documents": "விடுபட்ட ஆவணங்கள்",
    "Expiring Documents": "காலாவதியாகும் ஆவணங்கள்",
    "Upcoming Deadlines": "வரவிருக்கும் காலக்கெடு",
    "MY NEXT ACTION": "எனது அடுத்த நடவடிக்கை",
    "Step 1: Gather Required Documents": "படி 1: தேவையான ஆவணங்களை சேகரிக்கவும்",
    "Apply on Official Portal": "அதிகாரப்பூர்வ இணையதளத்தில் விண்ணப்பிக்கவும்",
    "RECOMMENDED": "பரிந்துரைக்கப்பட்டது",
    "APPLICATION READINESS": "விண்ணப்பத் தயார்நிலை",
    "View Details": "விவரங்களைக் காண்க",
    "Readiness Score": "தயார்நிலை மதிப்பீடு",
    "Apply on .gov.in": ".gov.in இல் விண்ணப்பிக்கவும்",
    "Compare": "ஒப்பீடு",
    "Why Recommended for You": "உங்களுக்கு ஏன் பரிந்துரைக்கப்படுகிறது",
    "Document Gap Analysis": "ஆவண இடைவெளி பகுப்பாய்வு",
    "Missing": "விடுபட்டது",
    "Filter by": "வடிகட்டு",
    "All Categories": "அனைத்து பிரிவுகள்",
    "Matching Schemes": "பொருந்தும் திட்டங்கள்",
    "Search matching schemes...": "திட்டங்களைத் தேடுங்கள்...",
    "All Government Schemes Catalogue": "அனைத்து அரசுத் திட்டங்களின் பட்டியல்",
    "Search by scheme name, keyword, category, ministry, or benefit...": "திட்டத்தின் பெயர், வகை அல்லது அமைச்சகம் மூலம் தேடுங்கள்...",
    "Close": "மூடு",
    "Save Profile & Recalculate Schemes": "சுயவிவரத்தை சேமித்து திட்டங்களை மீண்டும் கணக்கிடுங்கள்",
    "Report Missing Scheme": "விடுபட்ட திட்டத்தை தெரிவிக்கவும்"
  },
  "te": {
    "SchemeSaathi": "స్కీమ్ సాథీ",
    "Citizen Government Scheme Action Platform": "పౌర ప్రభుత్వ పథకాల వేదిక",
    "Verified .gov.in Registry": "ధృవీకరించబడిన .gov.in రిజిస్ట్రీ",
    "I Need Help (Grievance Desk)": "సహాయం కావాలి (ఫిర్యాదుల డెస్క్)",
    "Official Security Notice:": "అధికారిక భద్రతా నోటీసు:",
    "SchemeSaathi will NEVER ask for your government portal passwords, OTP, or UPI PIN. Beware of unofficial agents.": "స్కీమ్ సాథీ ఎప్పటికీ పాస్‌వర్డ్, OTP లేదా UPI PIN అడగదు.",
    "All Government Schemes": "అన్ని ప్రభుత్వ పథకాలు",
    "For Me (Eligible)": "నా కోసం (అర్హత ఉన్నవి)",
    "My Documents": "నా పత్రాలు",
    "My Applications": "నా దరఖాస్తులు",
    "Comparison": "పోలిక",
    "Life-Events": "జీవిత సంఘటనలు",
    "Fraud Shield": "మోసం నిరోధం",
    "My Privacy": "నా గోప్యత",
    "Admin Registry": "అడ్మిన్ రిజిస్ట్రీ",
    "MY BENEFITS HEALTH CHECK": "నా పథకాల ఆరోగ్య తనిఖీ",
    "Live health status based on your profile and document readiness": "మీ ప్రొఫైల్ మరియు పత్రాల సంసిద్ధత ఆధారంగా స్థితి",
    "Eligible Schemes": "అర్హతగల పథకాలు",
    "High Priority": "అత్యధిక ప్రాధాన్యత",
    "Ready to Apply": "దరఖాస్తుకు సిద్ధం",
    "Applications In Progress": "పురోగతిలో ఉన్న దరఖాస్తులు",
    "Missing Documents": "అవసరమైన పత్రాలు",
    "Expiring Documents": "గడువు ముగిసే పత్రాలు",
    "Upcoming Deadlines": "రాబోయే గడువులు",
    "MY NEXT ACTION": "నా తదుపరి చర్య",
    "Step 1: Gather Required Documents": "దశ 1: అవసరమైన పత్రాలను సేకరించండి",
    "Apply on Official Portal": "అధికారిక పోర్టల్‌లో దరఖాస్తు చేసుకోండి",
    "RECOMMENDED": "సిఫార్సు చేయబడింది",
    "APPLICATION READINESS": "దరఖాస్తు సంసిద్ధత",
    "View Details": "వివరాలు చూడండి",
    "Readiness Score": "సంసిద్ధత స్కోర్",
    "Apply on .gov.in": ".gov.in లో దరఖాస్తు చేసుకోండి",
    "Compare": "పోలిక",
    "Why Recommended for You": "మీకు ఎందుకు సిఫార్సు చేయబడింది",
    "Document Gap Analysis": "పత్రాల కొరత విశ్లేషణ",
    "Missing": "కొరత",
    "Filter by": "ఫిల్టర్ చేయండి",
    "All Categories": "అన్ని విభాగాలు",
    "Matching Schemes": "సరిపోలే పథకాలు",
    "Search matching schemes...": "పథకాలను శోధించండి...",
    "All Government Schemes Catalogue": "అన్ని ప్రభుత్వ పథకాల కేటలాగ్",
    "Search by scheme name, keyword, category, ministry, or benefit...": "పథకం పేరు, వర్గం లేదా మంత్రిత్వ శాఖ ద్వారా శోధించండి...",
    "Close": "మూసివేయి",
    "Save Profile & Recalculate Schemes": "ప్రొఫైల్‌ను సేవ్ చేసి పథకాలను తిరిగి లెక్కించండి",
    "Report Missing Scheme": "మిస్ అయిన పథకాన్ని నివేదించండి"
  },
  "kn": {
    "SchemeSaathi": "ಸ್ಕೀಮ್ ಸಾಥಿ",
    "Citizen Government Scheme Action Platform": "ನಾಗರಿಕ ಸರ್ಕಾರಿ ಯೋಜನೆಗಳ ವೇದಿಕೆ",
    "Verified .gov.in Registry": "ಪರಿಶೀಲಿಸಿದ .gov.in ನೋಂದಣಿ",
    "I Need Help (Grievance Desk)": "ಸಹಾಯ ಬೇಕು (ದೂರು ಪರಿಹಾರ)",
    "Official Security Notice:": "ಅಧಿಕೃತ ಭದ್ರತಾ ಸೂಚನೆ:",
    "SchemeSaathi will NEVER ask for your government portal passwords, OTP, or UPI PIN. Beware of unofficial agents.": "ಸ್ಕೀಮ್ ಸಾಥಿ ಎಂದಿಗೂ ಪಾಸ್‌ವರ್ಡ್, OTP ಅಥವಾ UPI PIN ಕೇಳುವುದಿಲ್ಲ.",
    "All Government Schemes": "ಎಲ್ಲಾ ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು",
    "For Me (Eligible)": "ನನಗಾಗಿ (ಅರ್ಹ)",
    "My Documents": "ನನ್ನ ದಾಖಲೆಗಳು",
    "My Applications": "ನನ್ನ ಅರ್ಜಿಗಳು",
    "Comparison": "ಹೋಲಿಕೆ",
    "Life-Events": "ಜೀವನ ಘಟನೆಗಳು",
    "Fraud Shield": "ವಂಚನೆ ರಕ್ಷಣೆ",
    "My Privacy": "ನನ್ನ ಗೌಪ್ಯತೆ",
    "Admin Registry": "ನಿರ್ವಾಹಕ ನೋಂದಣಿ",
    "MY BENEFITS HEALTH CHECK": "ನನ್ನ ಯೋಜನೆ ಆರೋಗ್ಯ ತಪಾಸಣೆ",
    "Live health status based on your profile and document readiness": "ನಿಮ್ಮ ಪ್ರೊಫೈಲ್ ಮತ್ತು ದಾಖಲೆ ಸಿದ್ಧತೆಯ ಆಧಾರದ ಸ್ಥಿತಿ",
    "Eligible Schemes": "ಅರ್ಹ ಯೋಜನೆಗಳು",
    "High Priority": "ಹೆಚ್ಚಿನ ಆದ್ಯತೆ",
    "Ready to Apply": "ಅರ್ಜಿ ಸಲ್ಲಿಸಲು ಸಿದ್ಧ",
    "Applications In Progress": "ಪ್ರಗತಿಯಲ್ಲಿರುವ ಅರ್ಜಿಗಳು",
    "Missing Documents": "ಕಾಣೆಯಾದ ದಾಖಲೆಗಳು",
    "Expiring Documents": "ಅವಧಿ ಮುಗಿಯುವ ದಾಖಲೆಗಳು",
    "Upcoming Deadlines": "ಮುಂಬರುವ ಕೊನೆಯ ದಿನಾಂಕಗಳು",
    "MY NEXT ACTION": "ನನ್ನ ಮುಂದಿನ ಕ್ರಮ",
    "Step 1: Gather Required Documents": "ಹಂತ 1: ಅಗತ್ಯ ದಾಖಲೆಗಳನ್ನು ಸಂಗ್ರಹಿಸಿ",
    "Apply on Official Portal": "ಅಧಿಕೃತ ಪೋರ್ಟಲ್‌ನಲ್ಲಿ ಅರ್ಜಿ ಸಲ್ಲಿಸಿ",
    "RECOMMENDED": "ಶಿಫಾರಸು ಮಾಡಲಾಗಿದೆ",
    "APPLICATION READINESS": "ಅರ್ಜಿ ಸಿದ್ಧತೆ",
    "View Details": "ವಿವರಗಳನ್ನು ವೀಕ್ಷಿಸಿ",
    "Readiness Score": "ಸಿದ್ಧತೆ ಸ್ಕೋರ್",
    "Apply on .gov.in": ".gov.in ನಲ್ಲಿ ಅರ್ಜಿ ಸಲ್ಲಿಸಿ",
    "Compare": "ಹೋಲಿಕೆ",
    "Why Recommended for You": "ನಿಮಗಾಗಿ ಏಕೆ ಶಿಫಾರಸು ಮಾಡಲಾಗಿದೆ",
    "Document Gap Analysis": "ದಾಖಲೆ ಕೊರತೆ ವಿಶ್ಲೇಷಣೆ",
    "Missing": "ಕಾಣೆಯಾಗಿದೆ",
    "Filter by": "ಫಿಲ್ಟರ್ ಮಾಡಿ",
    "All Categories": "ಎಲ್ಲಾ ವರ್ಗಗಳು",
    "Matching Schemes": "ಹೊಂದಿಕೆಯಾಗುವ ಯೋಜನೆಗಳು",
    "Search matching schemes...": "ಯೋಜನೆಗಳನ್ನು ಹುಡುಕಿ...",
    "All Government Schemes Catalogue": "ಎಲ್ಲಾ ಸರ್ಕಾರಿ ಯೋಜನೆಗಳ ಪಟ್ಟಿ",
    "Search by scheme name, keyword, category, ministry, or benefit...": "ಯೋಜನೆಯ ಹೆಸರು, ವರ್ಗ ಅಥವಾ ಸಚಿವಾಲಯದ ಮೂಲಕ ಹುಡುಕಿ...",
    "Close": "ಮುಚ್ಚಿ",
    "Save Profile & Recalculate Schemes": "ಪ್ರೊಫೈಲ್ ಉಳಿಸಿ ಮತ್ತು ಯೋಜನೆಗಳನ್ನು ಮರು ಲೆಕ್ಕಾಚಾರ ಮಾಡಿ",
    "Report Missing Scheme": "ಕಾಣೆಯಾದ ಯೋಜನೆಯನ್ನು ವರದಿ ಮಾಡಿ"
  },
  "ml": {
    "SchemeSaathi": "സ്കീം സാഥി",
    "Citizen Government Scheme Action Platform": "പൗര സർക്കാർ പദ്ധതി വേദി",
    "Verified .gov.in Registry": "പരിശോധിച്ച .gov.in രജിസ്ട്രി",
    "I Need Help (Grievance Desk)": "സഹായം വേണം (പരാതി പരിഹാരം)",
    "Official Security Notice:": "ഔദ്യോഗിക സുരക്ഷാ അറിയിപ്പ്:",
    "SchemeSaathi will NEVER ask for your government portal passwords, OTP, or UPI PIN. Beware of unofficial agents.": "സ്കീം സാഥി ഒരിക്കലും പാസ്‌വേഡ്, OTP അല്ലെങ്കിൽ UPI PIN ചോദിക്കില്ല.",
    "All Government Schemes": "എല്ലാ സർക്കാർ പദ്ധതികളും",
    "For Me (Eligible)": "എനിക്കായി (അർഹമായവ)",
    "My Documents": "എന്റെ രേഖകൾ",
    "My Applications": "എന്റെ അപേക്ഷകൾ",
    "Comparison": "താരതമ്യം",
    "Life-Events": "ജീവിത സംഭവങ്ങൾ",
    "Fraud Shield": "തട്ടിപ്പ് പ്രതിരോധം",
    "My Privacy": "എന്റെ സ്വകാര്യത",
    "Admin Registry": "അഡ്മിൻ രജിസ്ട്രി",
    "MY BENEFITS HEALTH CHECK": "എന്റെ പദ്ധതി ആരോഗ്യ പരിശോധന",
    "Live health status based on your profile and document readiness": "നിങ്ങളുടെ പ്രൊഫൈലും രേഖാ സന്നദ്ധതയും അടിസ്ഥാനമാക്കിയുള്ള സ്ഥിതി",
    "Eligible Schemes": "അർഹമായ പദ്ധതികൾ",
    "High Priority": "ഉയർന്ന മുൻഗണന",
    "Ready to Apply": "അപേക്ഷിക്കാൻ തയ്യാർ",
    "Applications In Progress": "പുരോഗതിയിലുള്ള അപേക്ഷകൾ",
    "Missing Documents": "ലഭ്യമല്ലാത്ത രേഖകൾ",
    "Expiring Documents": "കാലഹരണപ്പെടുന്ന രേഖകൾ",
    "Upcoming Deadlines": "വരാനിരിക്കുന്ന സമയപരിധികൾ",
    "MY NEXT ACTION": "എന്റെ അടുത്ത നടപടി",
    "Step 1: Gather Required Documents": "ഘട്ടം 1: ആവശ്യമായ രേഖകൾ ശേഖരിക്കുക",
    "Apply on Official Portal": "ഔദ്യോഗിക പോർട്ടലിൽ അപേക്ഷിക്കുക",
    "RECOMMENDED": "ശുപാർശ ചെയ്യുന്നത്",
    "APPLICATION READINESS": "അപേക്ഷാ സന്നദ്ധത",
    "View Details": "വിശദാംശങ്ങൾ കാണുക",
    "Readiness Score": "സന്നദ്ധതാ സ്കോർ",
    "Apply on .gov.in": ".gov.in-ൽ അപേക്ഷിക്കുക",
    "Compare": "താരതമ്യം",
    "Why Recommended for You": "നിങ്ങൾക്ക് എന്തുകൊണ്ട് ശുപാർശ ചെയ്യുന്നു",
    "Document Gap Analysis": "രേഖാ കുറവ് വിശകലനം",
    "Missing": "ലഭ്യമല്ല",
    "Filter by": "ഫിൽട്ടർ ചെയ്യുക",
    "All Categories": "എല്ലാ വിഭാഗങ്ങളും",
    "Matching Schemes": "പൊരുത്തപ്പെടുന്ന പദ്ധതികൾ",
    "Search matching schemes...": "പദ്ധതികൾ തിരയുക...",
    "All Government Schemes Catalogue": "എല്ലാ സർക്കാർ പദ്ധതികളുടെയും കാറ്റലോഗ്",
    "Search by scheme name, keyword, category, ministry, or benefit...": "പദ്ധതിയുടെ പേര്, വിഭാഗം അല്ലെങ്കിൽ മന്ത്രാലയം വഴി തിരയുക...",
    "Close": "അടയ്ക്കുക",
    "Save Profile & Recalculate Schemes": "പ്രൊഫൈൽ സംരക്ഷിച്ച് പദ്ധതികൾ വീണ്ടും കണക്കാക്കുക",
    "Report Missing Scheme": "ലഭ്യമല്ലാത്ത പദ്ധതി റിപ്പോർട്ട് ചെയ്യുക"
  },
  "pa": {
    "SchemeSaathi": "ਸਕੀਮ ਸਾਥੀ",
    "Citizen Government Scheme Action Platform": "ਨਾਗਰਿਕ ਸਰਕਾਰੀ ਸਕੀਮ ਪਲੇਟਫਾਰਮ",
    "Verified .gov.in Registry": "ਪ੍ਰਮਾਣਿਤ .gov.in ਰਜਿਸਟਰੀ",
    "I Need Help (Grievance Desk)": "ਮਦਦ ਚਾਹੀਦੀ ਹੈ (ਸ਼ਿਕਾਇਤ ਡੈਸਕ)",
    "Official Security Notice:": "ਅਧਿਕਾਰਤ ਸੁਰੱਖਿਆ ਨੋਟਿਸ:",
    "SchemeSaathi will NEVER ask for your government portal passwords, OTP, or UPI PIN. Beware of unofficial agents.": "ਸਕੀਮ ਸਾਥੀ ਕਦੇ ਵੀ ਪਾਸਵਰਡ, OTP ਜਾਂ UPI PIN ਨਹੀਂ ਮੰਗੇਗਾ।",
    "All Government Schemes": "ਸਾਰੀਆਂ ਸਰਕਾਰੀ ਸਕੀਮਾਂ",
    "For Me (Eligible)": "ਮੇਰੇ ਲਈ (ਯੋਗ)",
    "My Documents": "ਮੇਰੇ ਦਸਤਾਵੇਜ਼",
    "My Applications": "ਮੇਰੀਆਂ ਅਰਜ਼ੀਆਂ",
    "Comparison": "ਤੁਲਨਾ",
    "Life-Events": "ਜੀਵਨ ਘਟਨਾਵਾਂ",
    "Fraud Shield": "ਧੋਖਾਧੜੀ ਸੁਰੱਖਿਆ",
    "My Privacy": "ਮੇਰੀ ਪਰਦੇਦਾਰੀ",
    "Admin Registry": "ਐਡਮਿਨ ਰਜਿਸਟਰੀ",
    "MY BENEFITS HEALTH CHECK": "ਮੇਰੀ ਸਕੀਮ ਸਿਹਤ ਜਾਂਚ",
    "Live health status based on your profile and document readiness": "ਤੁਹਾਡੀ ਪ੍ਰੋਫਾਈਲ ਅਤੇ ਦਸਤਾਵੇਜ਼ ਤਿਆਰੀ ਦੇ ਆਧਾਰ 'ਤੇ ਸਥਿਤੀ",
    "Eligible Schemes": "ਯੋਗ ਸਕੀਮਾਂ",
    "High Priority": "ਉੱਚ ਤਰਜੀਹ",
    "Ready to Apply": "ਅਰਜ਼ੀ ਦੇਣ ਲਈ ਤਿਆਰ",
    "Applications In Progress": "ਪ੍ਰਕਿਰਿਆ ਅਧੀਨ ਅਰਜ਼ੀਆਂ",
    "Missing Documents": "ਗੁੰਮ ਦਸਤਾਵੇਜ਼",
    "Expiring Documents": "ਮਿਆਦ ਪੁੱਗਣ ਵਾਲੇ ਦਸਤਾਵੇਜ਼",
    "Upcoming Deadlines": "ਆਉਣ ਵਾਲੀਆਂ ਆਖਰੀ ਮਿਤੀਆਂ",
    "MY NEXT ACTION": "ਮੇਰਾ ਅਗਲਾ ਕਦਮ",
    "Step 1: Gather Required Documents": "ਕਦਮ 1: ਲੋੜੀਂਦੇ ਦਸਤਾਵੇਜ਼ ਇਕੱਠੇ ਕਰੋ",
    "Apply on Official Portal": "ਅਧਿਕਾਰਤ ਪੋਰਟਲ 'ਤੇ ਅਰਜ਼ੀ ਦਿਓ",
    "RECOMMENDED": "ਸਿਫਾਰਸ਼ ਕੀਤੀ",
    "APPLICATION READINESS": "ਅਰਜ਼ੀ ਦੀ ਤਿਆਰੀ",
    "View Details": "ਵੇਰਵੇ ਦੇਖੋ",
    "Readiness Score": "ਤਿਆਰੀ ਸਕੋਰ",
    "Apply on .gov.in": ".gov.in 'ਤੇ ਅਰਜ਼ੀ ਦਿਓ",
    "Compare": "ਤੁਲਨਾ",
    "Why Recommended for You": "ਤੁਹਾਡੇ ਲਈ ਕਿਉਂ ਸਿਫਾਰਸ਼ ਕੀਤੀ ਗਈ",
    "Document Gap Analysis": "ਦਸਤਾਵੇਜ਼ ਘਾਟ ਵਿਸ਼ਲੇਸ਼ਣ",
    "Missing": "ਗੁੰਮ",
    "Filter by": "ਫਿਲਟਰ ਕਰੋ",
    "All Categories": "ਸਾਰੀਆਂ ਸ਼੍ਰੇਣੀਆਂ",
    "Matching Schemes": "ਮੇਲ ਖਾਂਦੀਆਂ ਸਕੀਮਾਂ",
    "Search matching schemes...": "ਸਕੀਮਾਂ ਖੋਜੋ...",
    "All Government Schemes Catalogue": "ਸਾਰੀਆਂ ਸਰਕਾਰੀ ਸਕੀਮਾਂ ਦੀ ਸੂਚੀ",
    "Search by scheme name, keyword, category, ministry, or benefit...": "ਸਕੀਮ ਦੇ ਨਾਮ, ਸ਼੍ਰੇਣੀ ਜਾਂ ਮੰਤਰਾਲੇ ਦੁਆਰਾ ਖੋਜੋ...",
    "Close": "ਬੰਦ ਕਰੋ",
    "Save Profile & Recalculate Schemes": "ਪ੍ਰੋਫਾਈਲ ਸੁਰੱਖਿਅਤ ਕਰੋ ਅਤੇ ਸਕੀਮਾਂ ਮੁੜ ਗਿਣੋ",
    "Report Missing Scheme": "ਗੁੰਮ ਸਕੀਮ ਦੀ ਰਿਪੋਰਟ ਕਰੋ"
  },
  "or": {
    "SchemeSaathi": "ସ୍କିମ୍ ସାଥୀ",
    "Citizen Government Scheme Action Platform": "ନାଗରିକ ସରକାରୀ ଯୋଜନା ମଞ୍ଚ",
    "Verified .gov.in Registry": "ଯାଞ୍ଚ ହୋଇଥିବା .gov.in ପଞ୍ଜିକା",
    "I Need Help (Grievance Desk)": "ସାହାଯ୍ୟ ଦରକାର (ଅଭିଯୋଗ ନିବାରଣ)",
    "Official Security Notice:": "ସରକାରୀ ସୁରକ୍ଷା ସୂଚନା:",
    "SchemeSaathi will NEVER ask for your government portal passwords, OTP, or UPI PIN. Beware of unofficial agents.": "ସ୍କିମ୍ ସାଥୀ କେବେ ବି ପାସୱାର୍ଡ, OTP କିମ୍ବା UPI PIN ମାଗିବ ନାହିଁ।",
    "All Government Schemes": "ସମସ୍ତ ସରକାରୀ ଯୋଜନା",
    "For Me (Eligible)": "ମୋ ପାଇଁ (ଯୋଗ୍ୟ)",
    "My Documents": "ମୋର ଦଲିଲ",
    "My Applications": "ମୋର ଆବେଦନ",
    "Comparison": "ତୁଳନା",
    "Life-Events": "ଜୀବନ ଘଟଣାବଳୀ",
    "Fraud Shield": "ଠକେଇ ସୁରକ୍ଷା",
    "My Privacy": "ମୋର ଗୋପନୀୟତା",
    "Admin Registry": "ପ୍ରଶାସକ ପଞ୍ଜିକା",
    "MY BENEFITS HEALTH CHECK": "ମୋ ଯୋଜନା ସ୍ୱାସ୍ଥ୍ୟ ଯାଞ୍ଚ",
    "Live health status based on your profile and document readiness": "ଆପଣଙ୍କ ପ୍ରୋଫାଇଲ୍ ଏବଂ ଦଲିଲ ପ୍ରସ୍ତୁତି ଆଧାରିତ ସ୍ଥିତି",
    "Eligible Schemes": "ଯୋଗ୍ୟ ଯୋଜନା",
    "High Priority": "ଉଚ୍ଚ ପ୍ରାଥମିକତା",
    "Ready to Apply": "ଆବେଦନ ପାଇଁ ପ୍ରସ୍ତୁତ",
    "Applications In Progress": "ପ୍ରକ୍ରିୟାଧୀନ ଆବେଦନ",
    "Missing Documents": "ଅନୁପସ୍ଥିତ ଦଲିଲ",
    "Expiring Documents": "ମିଆଦ ସରୁଥିବା ଦଲିଲ",
    "Upcoming Deadlines": "ଆଗାମୀ ଶେଷ ତାରିଖ",
    "MY NEXT ACTION": "ମୋ ପରବର୍ତ୍ତୀ ପଦକ୍ଷେପ",
    "Step 1: Gather Required Documents": "ପଦକ୍ଷେପ ୧: ଆବଶ୍ୟକ ଦଲିଲ ସଂଗ୍ରହ କରନ୍ତୁ",
    "Apply on Official Portal": "ସରକାରୀ ପୋର୍ଟାଲରେ ଆବେଦନ କରନ୍ତୁ",
    "RECOMMENDED": "ସୁପାରିଶ କରାଯାଇଛି",
    "APPLICATION READINESS": "ଆବେଦନ ପ୍ରସ୍ତୁତି",
    "View Details": "ବିବରଣୀ ଦେଖନ୍ତୁ",
    "Readiness Score": "ପ୍ରସ୍ତୁତି ସ୍କୋର",
    "Apply on .gov.in": ".gov.in ରେ ଆବେଦନ କରନ୍ତୁ",
    "Compare": "ତୁଳନା",
    "Why Recommended for You": "ଆପଣଙ୍କ ପାଇଁ କାହିଁକି ସୁପାରିଶ କରାଯାଇଛି",
    "Document Gap Analysis": "ଦଲିଲ ଅଭାବ ବିଶ୍ଳେଷଣ",
    "Missing": "ଅନୁପସ୍ଥିତ",
    "Filter by": "ଫିଲ୍ଟର୍ କରନ୍ତୁ",
    "All Categories": "ସମସ୍ତ ବର୍ଗ",
    "Matching Schemes": "ମେଳ ଖାଉଥିବା ଯୋଜନା",
    "Search matching schemes...": "ଯୋଜନା ଖୋଜନ୍ତୁ...",
    "All Government Schemes Catalogue": "ସମସ୍ତ ସରକାରୀ ଯୋଜନା ତାଲିକା",
    "Search by scheme name, keyword, category, ministry, or benefit...": "ଯୋଜନାର ନାମ, ବର୍ଗ କିମ୍ବା ମନ୍ତ୍ରଣାଳୟ ଦ୍ୱାରା ଖୋଜନ୍ତୁ...",
    "Close": "ବନ୍ଦ କରନ୍ତୁ",
    "Save Profile & Recalculate Schemes": "ପ୍ରୋଫାଇଲ୍ ସଂରକ୍ଷଣ କରନ୍ତୁ ଏବଂ ଯୋଜନା ପୁନଃଗଣନା କରନ୍ତୁ",
    "Report Missing Scheme": "ଅନୁପସ୍ଥିତ ଯୋଜନା ରିପୋର୍ଟ କରନ୍ତୁ"
  },
  "as": {
    "SchemeSaathi": "স্কিম সাৰথী",
    "Citizen Government Scheme Action Platform": "নাগৰিক চৰকাৰী আঁচনি মঞ্চ",
    "Verified .gov.in Registry": "প্ৰমাণিত .gov.in পঞ্জীয়ন",
    "I Need Help (Grievance Desk)": "সহায় লাগে (অভিযোগ বিভাগ)",
    "Official Security Notice:": "চৰকাৰী সুৰক্ষা জাননী:",
    "SchemeSaathi will NEVER ask for your government portal passwords, OTP, or UPI PIN. Beware of unofficial agents.": "স্কিম সাৰথীয়ে কেতিয়াও পাছৱৰ্ড, OTP বা UPI PIN নিবিচাৰে।",
    "All Government Schemes": "সকলো চৰকাৰী আঁচনি",
    "For Me (Eligible)": "মোৰ বাবে (যোগ্য)",
    "My Documents": "মোৰ নথিপত্ৰ",
    "My Applications": "মোৰ আবেদনসমূহ",
    "Comparison": "তুলনা",
    "Life-Events": "জীৱন ঘটনাৱলী",
    "Fraud Shield": "প্ৰতাৰণা সুৰক্ষা",
    "My Privacy": "মোৰ গোপনীয়তা",
    "Admin Registry": "প্ৰশাসক পঞ্জীয়ন",
    "MY BENEFITS HEALTH CHECK": "মোৰ আঁচনি স্বাস্থ্য পৰীক্ষা",
    "Live health status based on your profile and document readiness": "আপোনাৰ প্ৰফাইল আৰু নথি প্ৰস্তুতিৰ ওপৰত ভিত্তি কৰি স্থিতি",
    "Eligible Schemes": "যোগ্য আঁচনিসমূহ",
    "High Priority": "উচ্চ অগ্ৰাধিকাৰ",
    "Ready to Apply": "আবেদন কৰিবলৈ সাজু",
    "Applications In Progress": "প্ৰক্ৰিয়াধীন আবেদন",
    "Missing Documents": "অনুপস্থিত নথিপত্ৰ",
    "Expiring Documents": "ম্যাদ উকলিব লগা নথিপত্ৰ",
    "Upcoming Deadlines": "আসন্ন শেষ তাৰিখ",
    "MY NEXT ACTION": "মোৰ পৰৱৰ্তী পদক্ষেপ",
    "Step 1: Gather Required Documents": "পদক্ষেপ ১: প্ৰয়োজনীয় নথিপত্ৰ সংগ্ৰহ কৰক",
    "Apply on Official Portal": "চৰকাৰী পৰ্টেলত আবেদন কৰক",
    "RECOMMENDED": "পৰামৰ্শিত",
    "APPLICATION READINESS": "আবেদন প্ৰস্তুতি",
    "View Details": "বিৱৰণ চাওক",
    "Readiness Score": "প্ৰস্তুতি স্কোৰ",
    "Apply on .gov.in": ".gov.in ত আবেদন কৰক",
    "Compare": "তুলনা",
    "Why Recommended for You": "আপোনাৰ বাবে কিয় পৰামৰ্শ দিয়া হৈছে",
    "Document Gap Analysis": "নথি ঘাটি বিশ্লেষণ",
    "Missing": "অনুপস্থিত",
    "Filter by": "ফিল্টাৰ কৰক",
    "All Categories": "সকলো শ্ৰেণী",
    "Matching Schemes": "মিলা আঁচনিসমূহ",
    "Search matching schemes...": "আঁচনি সন্ধান কৰক...",
    "All Government Schemes Catalogue": "সকলো চৰকাৰী আঁচনিৰ তালিকা",
    "Search by scheme name, keyword, category, ministry, or benefit...": "আঁচনিৰ নাম, শ্ৰেণী বা মন্ত্ৰালয় অনুসৰি সন্ধান কৰক...",
    "Close": "বন্ধ কৰক",
    "Save Profile & Recalculate Schemes": "প্ৰফাইল সংৰক্ষণ কৰক আৰু আঁচনি পুনৰ গণনা কৰক",
    "Report Missing Scheme": "অনুপস্থিত আঁচনিৰ অভিযোগ দিয়ক"
  },
  "ur": {
    "SchemeSaathi": "اسکیم ساتھی",
    "Citizen Government Scheme Action Platform": "شہری سرکاری اسکیم پلیٹ فارم",
    "Verified .gov.in Registry": "تصدیق شدہ .gov.in رجسٹری",
    "I Need Help (Grievance Desk)": "مدد چاہیے (شکایات ڈیسک)",
    "Official Security Notice:": "سرکاری سیکیورٹی نوٹس:",
    "SchemeSaathi will NEVER ask for your government portal passwords, OTP, or UPI PIN. Beware of unofficial agents.": "اسکیم ساتھی کبھی پاس ورڈ، OTP یا UPI PIN نہیں مانگے گا۔",
    "All Government Schemes": "تمام سرکاری اسکیمیں",
    "For Me (Eligible)": "میرے لیے (اہل)",
    "My Documents": "میرے دستاویزات",
    "My Applications": "میری درخواستیں",
    "Comparison": "موازنہ",
    "Life-Events": "زندگی کے واقعات",
    "Fraud Shield": "فراڈ شیلڈ",
    "My Privacy": "میری پرائیویسی",
    "Admin Registry": "ایڈمن رجسٹری",
    "MY BENEFITS HEALTH CHECK": "میری اسکیم ہیلتھ چیک",
    "Live health status based on your profile and document readiness": "آپ کے پروفائل اور دستاویز کی تیاری پر مبنی لائیو حیثیت",
    "Eligible Schemes": "اہل اسکیمیں",
    "High Priority": "اعلیٰ ترجیح",
    "Ready to Apply": "درخواست کے لیے تیار",
    "Applications In Progress": "زیر عمل درخواستیں",
    "Missing Documents": "گم شدہ دستاویزات",
    "Expiring Documents": "ختم ہونے والی دستاویزات",
    "Upcoming Deadlines": "آنے والی آخری تاریخیں",
    "MY NEXT ACTION": "میرا اگلا اقدام",
    "Step 1: Gather Required Documents": "مرحلہ 1: ضروری دستاویزات جمع کریں",
    "Apply on Official Portal": "سرکاری پورٹل پر درخواست دیں",
    "RECOMMENDED": "تجویز کردہ",
    "APPLICATION READINESS": "درخواست کی تیاری",
    "View Details": "تفصیلات دیکھیں",
    "Readiness Score": "تیاری کا اسکور",
    "Apply on .gov.in": ".gov.in پر درخواست دیں",
    "Compare": "موازنہ",
    "Why Recommended for You": "آپ کے لیے کیوں تجویز کردہ",
    "Document Gap Analysis": "دستاویزات کی کمی کا تجزیہ",
    "Missing": "لاپتہ",
    "Filter by": "فلٹر کریں",
    "All Categories": "تمام زمرے",
    "Matching Schemes": "مطابقت رکھنے والی اسکیمیں",
    "Search matching schemes...": "اسکیمیں تلاش کریں...",
    "All Government Schemes Catalogue": "تمام سرکاری اسکیموں کی کیٹلاگ",
    "Search by scheme name, keyword, category, ministry, or benefit...": "اسکیم کے نام، زمرے یا وزارت کے ذریعہ تلاش کریں...",
    "Close": "بند کریں",
    "Save Profile & Recalculate Schemes": "پروفائل محفوظ کریں اور اسکیموں کا دوبارہ حساب لگائیں",
    "Report Missing Scheme": "لاپتہ اسکیم کی اطلاع دیں"
  },
  "sa": {
    "SchemeSaathi": "योजना साथी",
    "Citizen Government Scheme Action Platform": "नागरिक सर्वकारीययोजना कार्यपीठिका",
    "Verified .gov.in Registry": "सत्यापिता .gov.in पञ्जिका",
    "I Need Help (Grievance Desk)": "साहाय्यम् आवश्यकम्",
    "Official Security Notice:": "आधिकारिक सुरक्षा सूचना:",
    "SchemeSaathi will NEVER ask for your government portal passwords, OTP, or UPI PIN. Beware of unofficial agents.": "योजना साथी कदापि पासवर्ड, OTP वा UPI PIN न याचते।",
    "All Government Schemes": "सर्वाः सर्वकारीययोजनाः",
    "For Me (Eligible)": "मम कृते (योग्याः)",
    "My Documents": "मम प्रलेखाः",
    "My Applications": "मम आवेदनानि",
    "Comparison": "तुलना",
    "Life-Events": "जीवन-घटनाः",
    "Fraud Shield": "वञ्चना संरक्षणम्",
    "My Privacy": "मम गोपनीयता",
    "Admin Registry": "प्रशासक पञ्जिका",
    "MY BENEFITS HEALTH CHECK": "मम योजना स्वास्थ्य परीक्षणम्",
    "Live health status based on your profile and document readiness": "भवतां विवरणपत्रं प्रलेखसज्जताञ्च आधृत्य प्रत्यक्षस्थितिः",
    "Eligible Schemes": "योग्याः योजनाः",
    "High Priority": "उच्चप्राथमिकता",
    "Ready to Apply": "आवेदनाय सिद्धाः",
    "Applications In Progress": "प्रक्रियारतानि आवेदनानि",
    "Missing Documents": "अनुपलब्धाः प्रलेखाः",
    "Expiring Documents": "समाप्तप्रायाः प्रलेखाः",
    "Upcoming Deadlines": "आगामिन्यः अन्तिमतिथयः",
    "MY NEXT ACTION": "मम अग्रिमं कार्यम्",
    "Step 1: Gather Required Documents": "प्रथमः चरणः: अपेक्षितान् प्रलेखान् सङ्गृह्णन्तु",
    "Apply on Official Portal": "आधिकारिकजालपुटे आवेदनं कुर्वन्तु",
    "RECOMMENDED": "अनुशंसितम्",
    "APPLICATION READINESS": "आवेदन सज्जता",
    "View Details": "विवरणं पश्यन्तु",
    "Readiness Score": "सज्जताङ्कः",
    "Apply on .gov.in": ".gov.in मध्ये आवेदनं कुर्वन्तु",
    "Compare": "तुलना",
    "Why Recommended for You": "भवतां कृते किमर्थम् अनुशंसितम्",
    "Document Gap Analysis": "प्रलेखन्यूनता विश्लेषणम्",
    "Missing": "अनुपलब्धम्",
    "Filter by": "शोधनं कुर्वन्तु",
    "All Categories": "सर्वे वर्गाः",
    "Matching Schemes": "अनुरूपाः योजनाः",
    "Search matching schemes...": "योजनाः अन्विषन्तु...",
    "All Government Schemes Catalogue": "सर्वासाम् सर्वकारीययोजनानां सूची",
    "Search by scheme name, keyword, category, ministry, or benefit...": "योजनानाम, वर्गः वा मन्त्रालयेन अन्विषन्तु...",
    "Close": "पिदधतु",
    "Save Profile & Recalculate Schemes": "विवरणपत्रं संरक्ष्य योजनानां पुनर्गणनं कुर्वन्तु",
    "Report Missing Scheme": "अनुपलब्धयोजनां सूचयन्तु"
  },
  "kok": {
    "SchemeSaathi": "स्कीम साथी",
    "Citizen Government Scheme Action Platform": "नागरीक सरकारी येवजण मंच",
    "Verified .gov.in Registry": "तपासलेली .gov.in नोंदणी",
    "I Need Help (Grievance Desk)": "मदत जाय (गाऱ्हाणी केंद्र)",
    "Official Security Notice:": "अधिकृत सुरक्षा सुचोवणी:",
    "SchemeSaathi will NEVER ask for your government portal passwords, OTP, or UPI PIN. Beware of unofficial agents.": "स्कीम साथी केन्नाच पासवर्ड, OTP वा UPI PIN मागचो ना.",
    "All Government Schemes": "सगळ्यो सरकारी येवजण्यो",
    "For Me (Eligible)": "म्हजे खातीर (पात्र)",
    "My Documents": "म्हजे दस्तावेज",
    "My Applications": "म्हजे अर्ज",
    "Comparison": "तुलना",
    "Life-Events": "जीण-घडणुको",
    "Fraud Shield": "फसवणूक राखण",
    "My Privacy": "म्हजी गुप्तता",
    "Admin Registry": "प्रशासक नोंदणी",
    "MY BENEFITS HEALTH CHECK": "म्हजी येवजण भलायकी तपासणी",
    "Live health status based on your profile and document readiness": "तुमच्या प्रोफायल आनी दस्तावेज तयारीचेर आदारीत स्थिती",
    "Eligible Schemes": "पात्र येवजण्यो",
    "High Priority": "उंच प्राधान्य",
    "Ready to Apply": "अर्ज करपाक तयार",
    "Applications In Progress": "प्रक्रियेंतले अर्ज",
    "Missing Documents": "उणे दस्तावेज",
    "Expiring Documents": "कालबाह्य जावपी दस्तावेज",
    "Upcoming Deadlines": "मुखेल निमाण्यो तारखो",
    "MY NEXT ACTION": "म्हजी फुडली कृती",
    "Step 1: Gather Required Documents": "पांवलो १: गरजेचे दस्तावेज एकठांय करात",
    "Apply on Official Portal": "अधिकृत पोर्टलाचेर अर्ज करात",
    "RECOMMENDED": "शिफारस केल्ली",
    "APPLICATION READINESS": "अर्ज तयारी",
    "View Details": "तपशील पळेयात",
    "Readiness Score": "तयारी गुण",
    "Apply on .gov.in": ".gov.in चेर अर्ज करात",
    "Compare": "तुलना",
    "Why Recommended for You": "तुमच्या खातीर शिफारस कित्याक",
    "Document Gap Analysis": "दस्तावेज उणेपण विश्लेषण",
    "Missing": "उणे",
    "Filter by": "फिल्टर करात",
    "All Categories": "सगळ्यो वर्गवारी",
    "Matching Schemes": "जुळपी येवजण्यो",
    "Search matching schemes...": "येवजण्यो सोधात...",
    "All Government Schemes Catalogue": "सगळ्या सरकारी येवजण्यांची वळेरी",
    "Search by scheme name, keyword, category, ministry, or benefit...": "येवजणेचें नांव, वर्ग वा मंत्रालया प्रमाण सोधात...",
    "Close": "बंद करात",
    "Save Profile & Recalculate Schemes": "प्रोफायल सांबाळात आनी येवजण्यो परतून तपासात",
    "Report Missing Scheme": "सुटलेली येवजण नोंदयात"
  }
};


  const KEY_MAP = {
    "nav.allSchemes": "All Government Schemes",
    "nav.forMe": "For Me (Eligible)",
    "nav.vault": "My Documents",
    "nav.applications": "My Applications",
    "nav.compare": "Comparison",
    "nav.lifeEvents": "Life-Events",
    "nav.fraudShield": "Fraud Shield",
    "nav.privacy": "My Privacy",
    "nav.admin": "Admin Registry"
  };

  class SchemeSaathiI18n {
    constructor() {
      this.currentLang = localStorage.getItem('schemesaathi_lang') || 'en';
      this.phraseMaps = PHRASE_MAPS;
    }

    t(key, fallback = '') {
      if (!key) return fallback;
      const lang = this.currentLang || 'en';
      const targetMap = this.phraseMaps[lang] || this.phraseMaps.en || {};
      if (targetMap[key]) return targetMap[key];
      if (KEY_MAP[key] && targetMap[KEY_MAP[key]]) {
        return targetMap[KEY_MAP[key]];
      }
      return fallback || (KEY_MAP[key] ? KEY_MAP[key] : key);
    }

    translateNode(node, lang) {
      if (!node) return;

      // 1. Text Node translation
      if (node.nodeType === 3) {
        const text = node.textContent.trim();
        if (!text || text.length <= 1) return;

        if (!node._origText) {
          node._origText = text;
        }

        const orig = node._origText;
        const targetMap = this.phraseMaps[lang];

        if (lang === 'en' && node._origText) {
          node.textContent = node.textContent.replace(text, node._origText);
        } else if (targetMap && targetMap[orig]) {
          node.textContent = node.textContent.replace(text, targetMap[orig]);
        }
        return;
      }

      // 2. Element Node translation
      if (node.nodeType === 1) {
        const tag = node.tagName.toUpperCase();
        if (tag === 'SCRIPT' || tag === 'STYLE' || tag === 'CODE' || tag === 'PRE' || tag === 'OPTION') return;

        // Attribute: data-i18n
        const i18nKey = node.getAttribute('data-i18n');
        if (i18nKey) {
          const trans = this.t(i18nKey, null);
          if (trans) {
            node.textContent = trans;
            return;
          }
        }

        // Input Placeholder translation
        if (node.placeholder) {
          if (!node._origPlaceholder) {
            node._origPlaceholder = node.placeholder.trim();
          }
          const origPh = node._origPlaceholder;
          const targetMap = this.phraseMaps[lang];
          if (lang === 'en' && node._origPlaceholder) {
            node.placeholder = node._origPlaceholder;
          } else if (targetMap && targetMap[origPh]) {
            node.placeholder = targetMap[origPh];
          }
        }

        // Title translation
        if (node.title) {
          if (!node._origTitle) {
            node._origTitle = node.title.trim();
          }
          const origTitle = node._origTitle;
          const targetMap = this.phraseMaps[lang];
          if (lang === 'en' && node._origTitle) {
            node.title = node._origTitle;
          } else if (targetMap && targetMap[origTitle]) {
            node.title = targetMap[origTitle];
          }
        }

        // Recursively translate all children
        const children = node.childNodes;
        for (let i = 0; i < children.length; i++) {
          this.translateNode(children[i], lang);
        }
      }
    }

    updateAiStaticText(lang) {
      const welcomeTitle = document.getElementById('ai-welcome-title');
      const welcomeDesc = document.getElementById('ai-welcome-desc');
      const inputEl = document.getElementById('ai-input');
      const presetContainer = document.getElementById('ai-preset-chips');

      const AI_TEXTS = {
        "en": {
          "title": "Namaste! I am your personal SchemeSaathi AI Copilot.",
          "desc": "I am aware of your profile, missing documents, and eligible schemes. I strictly use verified official government data (.gov.in) and never hallucinate non-existent programs or links.",
          "placeholder": "Ask a question about government schemes in your preferred language...",
          "chips": ["What schemes am I eligible for?", "Which scheme should I apply for first?", "What document am I missing?"]
        },
        "hi": {
          "title": "नमस्ते! मैं आपका निजी स्कीम साथी AI सहायक हूँ।",
          "desc": "मैं आपकी प्रोफ़ाइल, अनुपलब्ध दस्तावेज़ों और पात्र योजनाओं से पूरी तरह अवगत हूँ। मैं केवल सत्यापित सरकारी डेटा (.gov.in) का उपयोग करता हूँ।",
          "placeholder": "अपनी पसंदीदा भाषा में सरकारी योजनाओं के बारे में प्रश्न पूछें...",
          "chips": ["मुझे कौन सी सरकारी योजनाएं मिल सकती हैं?", "मुझे सबसे पहले किस योजना में आवेदन करना चाहिए?", "मेरा कौन सा दस्तावेज़ बाकी है?"]
        },
        "mr": {
          "title": "नमस्कार! मी तुमचा वैयक्तिक स्कीम साथी AI मार्गदर्शक आहे.",
          "desc": "मी तुमच्या नागरिक प्रोफाइल आणि व्हॉल्ट दस्तऐवजांनुसार पात्र योजना शोधतो. मी केवळ अधिकृत सरकारी माहिती (.gov.in) वापरतो.",
          "placeholder": "योजना, कागदपत्रे, किंवा अर्जाबद्दल विचारा...",
          "chips": ["मला कोणत्या योजना मिळतील?", "मी आधी कोणत्या योजनेसाठी अर्ज करावा?", "माझे कोणते कागदपत्र अपूर्ण आहे?"]
        },
        "bn": {
          "title": "নমস্কার! আমি আপনার ব্যক্তিগত স্কিম সাথী AI সহকারী।",
          "desc": "আমি আপনার প্রোফাইল, নথিপত্র এবং যোগ্য স্কিম সম্পর্কে অবগত।",
          "placeholder": "সরকারি স্কিম সম্পর্কে প্রশ্ন জিজ্ঞাসা করুন...",
          "chips": ["আমি কোন স্কিমের জন্য যোগ্য?", "প্রথমে কোন স্কিমে আবেদন করব?", "আমার কোন নথি বাকি আছে?"]
        },
        "gu": {
          "title": "નમસ્તે! હું તમારો વ્યક્તિગત સ્કીમ સાથી AI સહાયક છું.",
          "desc": "હું તમારી પ્રોફાઇલ, દસ્તાવેજો અને પાત્ર યોજનાઓથી વાકેફ છું.",
          "placeholder": "સરકારી યોજનાઓ વિશે પ્રશ્ન પૂછો...",
          "chips": ["મને કઈ યોજનાઓ મળી શકે?", "પહેલા કઈ યોજના માટે અરજી કરવી?", "મારો કયો દસ્તાવેજ ખૂટે છે?"]
        },
        "ta": {
          "title": "வணக்கம்! நான் உங்கள் தனிப்பட்ட ஸ்கீம் சாதி AI உதவியாளர்.",
          "desc": "உங்கள் சுயவிவரம் மற்றும் தகுதியான திட்டங்களை நான் அறிவேன்.",
          "placeholder": "அரசுத் திட்டங்கள் பற்றி கேளுங்கள்...",
          "chips": ["நான் என்ன திட்டங்களுக்கு தகுதியானவன்?", "முதலில் எதற்கு விண்ணப்பிக்க வேண்டும்?", "எந்த ஆவணம் விடுபட்டுள்ளது?"]
        },
        "te": {
          "title": "నమస్కారం! నేను మీ వ్యక్తిగత స్కీమ్ సాథీ AI సహాయకుడిని.",
          "desc": "మీ ప్రొఫైల్ మరియు అర్హతగల పథకాల గురించి నాకు తెలుసు.",
          "placeholder": "ప్రభుత్వ పథకాల గురించి ప్రశ్నలు అడగండి...",
          "chips": ["నాకు ఏ పథకాలు లభిస్తాయి?", "మొదట దేనికి దరఖాస్తు చేయాలి?", "నాకు ఏ పత్రం కొరత ఉంది?"]
        },
        "kn": {
          "title": "ನಮಸ್ಕಾರ! ನಾನು ನಿಮ್ಮ ವೈಯಕ್ತಿಕ ಸ್ಕೀಮ್ ಸಾಥಿ AI ಸಹಾಯಕ.",
          "desc": "ನಿಮ್ಮ ಪ್ರೊಫೈಲ್ ಮತ್ತು ಅರ್ಹ ಯೋಜನೆಗಳ ಬಗ್ಗೆ ನನಗೆ ತಿಳಿದಿದೆ.",
          "placeholder": "ಸರ್ಕಾರಿ ಯೋಜನೆಗಳ ಬಗ್ಗೆ ಕೇಳಿ...",
          "chips": ["ನನಗೆ ಯಾವ ಯೋಜನೆಗಳು ಸಿಗುತ್ತವೆ?", "ಮೊದಲು ಯಾವುದಕ್ಕೆ ಅರ್ಜಿ ಸಲ್ಲಿಸಬೇಕು?", "ನನ್ನ ಯಾವ ದಾಖಲೆ ಬಾಕಿ ಇದೆ?"]
        },
        "ml": {
          "title": "നമസ്കാരം! ഞാൻ നിങ്ങളുടെ വ്യക്തിഗത സ്കീം സാഥി AI സഹായിയാണ്.",
          "desc": "നിങ്ങളുടെ പ്രൊഫൈലും അർഹമായ പദ്ധതികളും എനിക്കറിയാം.",
          "placeholder": "പദ്ധതികളെക്കുറിച്ച് ചോദിക്കുക...",
          "chips": ["എനിക്ക് എന്ത് പദ്ധതികൾ ലഭിക്കും?", "ആദ്യം ഏതിന് അപേക്ഷിക്കണം?", "എന്റെ ഏത് രേഖയാണ് ലഭ്യമല്ലാത്തത്?"]
        },
        "pa": {
          "title": "ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ! ਮੈਂ ਤੁਹਾਡਾ ਨਿੱਜੀ ਸਕੀਮ ਸਾਥੀ AI ਸਹਾਇਕ ਹਾਂ।",
          "desc": "ਮੈਂ ਤੁਹਾਡੀ ਪ੍ਰੋਫਾਈਲ ਅਤੇ ਯੋਗ ਸਕੀਮਾਂ ਤੋਂ ਜਾਣੂ ਹਾਂ।",
          "placeholder": "ਸਰਕਾਰੀ ਸਕੀਮਾਂ ਬਾਰੇ ਸਵਾਲ ਪੁੱਛੋ...",
          "chips": ["ਮੈਨੂੰ ਕਿਹੜੀਆਂ ਸਕੀਮਾਂ ਮਿਲ ਸਕਦੀਆਂ ਹਨ?", "ਮੈਨੂੰ ਪਹਿਲਾਂ ਕਿਸ ਲਈ ਅਰਜ਼ੀ ਦੇਣੀ ਚਾਹੀਦੀ ਹੈ?", "ਮੇਰਾ ਕਿਹੜਾ ਦਸਤਾਵੇਜ਼ ਬਾਕੀ ਹੈ?"]
        },
        "or": {
          "title": "ନମସ୍କାର! ମୁଁ ଆପଣଙ୍କ ବ୍ୟକ୍ତିଗତ ସ୍କିମ୍ ସାଥୀ AI ସହାୟକ।",
          "desc": "ମୁଁ ଆପଣଙ୍କ ପ୍ରୋଫାଇଲ୍ ଏବଂ ଯୋଗ୍ୟ ଯୋଜନା ବିଷୟରେ ଅବଗତ।",
          "placeholder": "ସରକାରୀ ଯୋଜନା ବିଷୟରେ ପଚାରନ୍ତୁ...",
          "chips": ["ମୋତେ କେଉଁ ଯୋଜନା ମିଳିପାରିବ?", "ମୁଁ ପ୍ରଥମେ କାହା ପାଇଁ ଆବେଦନ କରିବି?", "ମୋର କେଉଁ ଦଲିଲ ବାକି ଅଛି?"]
        },
        "as": {
          "title": "নমস্কাৰ! মই আপোনাৰ ব্যক্তিগত স্কিম সাৰথী AI সহায়ক।",
          "desc": "মই আপোনাৰ প্ৰফাইল আৰু যোগ্য আঁচনিসমূহৰ বিষয়ে অৱগত।",
          "placeholder": "চৰকাৰী আঁচনি সম্পৰ্কে সোধক...",
          "chips": ["মই কি আঁচনি পাম?", "প্ৰথমে কোনখন আঁচনিত আবেদন কৰিম?", "মোৰ কি নথি বাকী আছে?"]
        },
        "ur": {
          "title": "سلام! میں آپ کا ذاتی اسکیم ساتھی AI معاون ہوں۔",
          "desc": "میں آپ کے پروفائل اور اہل اسکیموں سے باخبر ہوں۔",
          "placeholder": "سرکاری اسکیموں کے بارے میں پوچھیں...",
          "chips": ["مجھے کون سی اسکیمیں مل سکتی ہیں؟", "مجھے پہلے کس میں درخواست دینی چاہیے؟", "میری کون سی دستاویز باقی ہے؟"]
        },
        "sa": {
          "title": "नमस्ते! अहं भवतां व्यक्तिगत योजना साथी AI सहायकोऽस्मि।",
          "desc": "अहं भवतां विवरणपत्रं योग्याः योजनाश्च जानामि।",
          "placeholder": "सर्वकारीययोजनानां विषये पृच्छन्तु...",
          "chips": ["मम कृते काः योजनाः सन्ति?", "प्रथमं कस्यां योजनायां आवेदनं कुर्याम्?", "मम कः प्रलेखः अवशिष्टः?"]
        },
        "kok": {
          "title": "नमस्कार! हांव तुमचो वैयक्तिक स्कीम साथी AI मार्गदर्शक.",
          "desc": "तुमच्या प्रोफायला प्रमाण पात्र येवजण्यांची म्हाका म्हायती आसा.",
          "placeholder": "सरकारी येवजण्यां विशीं विचारात...",
          "chips": ["म्हाका खंयच्यो येवजण्यो मेळटल्यो?", "पयलीं खंयचे येवजणेक अर्ज करचो?", "म्हजो खंयचो दस्तावेज उणो आसा?"]
        }
      };

      const config = AI_TEXTS[lang] || AI_TEXTS.en;
      if (welcomeTitle) welcomeTitle.textContent = config.title;
      if (welcomeDesc) welcomeDesc.textContent = config.desc;
      if (inputEl) inputEl.placeholder = config.placeholder;
      if (presetContainer && config.chips) {
        presetContainer.innerHTML = config.chips.map(chip => `
          <button onclick="askAiPreset('${escapeHtml(chip)}')" class="bg-white border border-indigo-200 text-indigo-800 px-2 py-1 rounded-full font-semibold hover:bg-indigo-50">"${escapeHtml(chip)}"</button>
        `).join('');
      }
    }

    setLanguage(lang) {
      this.currentLang = lang;
      localStorage.setItem('schemesaathi_lang', lang);
      document.documentElement.lang = lang;

      // Sync language select dropdowns
      const hSelect = document.getElementById('lang-select');
      if (hSelect && hSelect.value !== lang) hSelect.value = lang;
      const aiSelect = document.getElementById('ai-lang-select');
      if (aiSelect && aiSelect.value !== lang) aiSelect.value = lang;

      // Full DOM text node & placeholder translation
      this.translateNode(document.body, lang);

      // AI Copilot text translation
      this.updateAiStaticText(lang);
    }
  }

  function escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  window.i18n = new SchemeSaathiI18n();

  document.addEventListener('DOMContentLoaded', function() {
    const saved = localStorage.getItem('schemesaathi_lang') || 'en';
    window.i18n.setLanguage(saved);
  });

})(window);
