/**
 * SchemeSaathi - 15 Indian Languages Native Multilingual Engine
 * Zero external dependencies, pure vanilla JS dictionary & instant DOM binder.
 */

(function(window) {
  'use strict';

  const LOCALES = {
  "en": {
    "appTitle": "SchemeSaathi",
    "appSubtitle": "Citizen Government Scheme & Document Action Engine",
    "safetyNotice": "Official Security Notice: SchemeSaathi will NEVER ask for your government portal passwords, OTP, or UPI PIN. Beware of unofficial agents.",
    "nav": {
      "allSchemes": "All Government Schemes",
      "forMe": "For Me (Eligible)",
      "vault": "My Documents",
      "applications": "My Applications",
      "compare": "Compare",
      "lifeEvents": "Life-Events",
      "fraudShield": "Fraud Shield",
      "privacy": "My Privacy",
      "admin": "Admin Registry"
    },
    "healthCheck": {
      "title": "MY BENEFITS HEALTH CHECK",
      "subtitle": "Live health status based on your profile and document readiness",
      "eligible": "Eligible Schemes",
      "highPriority": "High Priority",
      "readyToApply": "Ready to Apply",
      "inProgress": "Applications In Progress",
      "missingDocs": "Missing Documents",
      "expiringDocs": "Expiring Documents",
      "upcomingDeadlines": "Upcoming Deadlines"
    },
    "nextAction": {
      "title": "MY NEXT ACTION",
      "readyNow": "READY NOW",
      "step": "Step 1: Gather Required Documents",
      "applyButton": "Apply on Official Portal"
    },
    "schemeCard": {
      "recommended": "RECOMMENDED",
      "verified": "Official .gov.in",
      "benefit": "Benefit",
      "deadline": "Deadline",
      "readiness": "APPLICATION READINESS",
      "compare": "Compare",
      "viewDetails": "View Details",
      "readinessScore": "Readiness Score",
      "applyNow": "Apply on .gov.in",
      "whyRecommended": "Why Recommended for You",
      "documentGap": "Document Gap Analysis",
      "missing": "Missing"
    },
    "ui": {
      "startMyProfile": "Start My Profile",
      "exploreAllSchemes": "Explore All Schemes",
      "findSchemesForMe": "Find Schemes For Me",
      "reportMissingScheme": "Report Missing Scheme",
      "saveProfileRecalculate": "Save Profile & Recalculate Schemes",
      "filterBy": "Filter by",
      "allCategories": "All Categories",
      "matchingSchemes": "Matching Schemes",
      "searchPlaceholder": "Search matching schemes...",
      "allSchemesCatalogue": "All Government Schemes Catalogue",
      "searchCatalogue": "Search by scheme name, keyword, category, ministry, or benefit..."
    },
    "ai": {
      "welcomeTitle": "Namaste! I am your personal SchemeSaathi AI Copilot.",
      "welcomeDesc": "I am aware of your profile, missing documents, and eligible schemes. I strictly use verified official government data (.gov.in) and never hallucinate non-existent programs or links.",
      "inputPlaceholder": "Ask a question about government schemes in your preferred language...",
      "chip1": "What schemes am I eligible for?",
      "chip2": "Which scheme should I apply for first?",
      "chip3": "What document am I missing?"
    }
  },
  "hi": {
    "appTitle": "स्कीम साथी",
    "appSubtitle": "नागरिक सरकारी योजना एवं दस्तावेज़ सहायता इंजन",
    "safetyNotice": "आधिकारिक सुरक्षा सूचना: स्कीम साथी आपसे कभी भी सरकारी पोर्टल पासवर्ड, ओटीपी या यूपीआई पिन नहीं मांगेगा। अनाधिकृत एजेंटों से सावधान रहें।",
    "nav": {
      "allSchemes": "सभी सरकारी योजनाएं",
      "forMe": "मेरे लिए (पात्र)",
      "vault": "मेरे दस्तावेज़",
      "applications": "मेरे आवेदन",
      "compare": "तुलना करें",
      "lifeEvents": "जीवन-घटनाएं",
      "fraudShield": "धोखाधड़ी सुरक्षा",
      "privacy": "मेरी गोपनीयता",
      "admin": "व्यवस्थापक रजिस्ट्री"
    },
    "healthCheck": {
      "title": "मेरी योजना स्वास्थ्य जांच",
      "subtitle": "आपकी प्रोफ़ाइल और दस्तावेज़ तत्परता के आधार पर वास्तविक स्वास्थ्य स्थिति",
      "eligible": "पात्र योजनाएं",
      "highPriority": "उच्च प्राथमिकता",
      "readyToApply": "आवेदन के लिए तैयार",
      "inProgress": "प्रक्रियाधीन आवेदन",
      "missingDocs": "अनुपलब्ध दस्तावेज़",
      "expiringDocs": "समाप्त होने वाले दस्तावेज़",
      "upcomingDeadlines": "आगामी अंतिम तिथियां"
    },
    "nextAction": {
      "title": "मेरा अगला कदम",
      "readyNow": "अभी तैयार",
      "step": "कदम 1: आवश्यक दस्तावेज़ एकत्र करें",
      "applyButton": "आधिकारिक पोर्टल पर आवेदन करें"
    },
    "schemeCard": {
      "recommended": "अनुशंसित",
      "verified": "सत्यापित .gov.in",
      "benefit": "लाभ",
      "deadline": "अंतिम तिथि",
      "readiness": "आवेदन तत्परता",
      "compare": "तुलना करें",
      "viewDetails": "विवरण देखें",
      "readinessScore": "तत्परता स्कोर",
      "applyNow": ".gov.in पर आवेदन करें",
      "whyRecommended": "आपके लिए अनुशंसित क्यों",
      "documentGap": "दस्तावेज़ अंतर विश्लेषण",
      "missing": "अनुपलब्ध"
    },
    "ui": {
      "startMyProfile": "मेरी प्रोफ़ाइल शुरू करें",
      "exploreAllSchemes": "सभी योजनाएं देखें",
      "findSchemesForMe": "मेरे लिए योजनाएं खोजें",
      "reportMissingScheme": "अनुपलब्ध योजना की रिपोर्ट करें",
      "saveProfileRecalculate": "प्रोफ़ाइल सहेजें और योजनाएं पुनर्गणना करें",
      "filterBy": "फ़िल्टर करें",
      "allCategories": "सभी श्रेणियां",
      "matchingSchemes": "मिलान योजनाएं",
      "searchPlaceholder": "योजनाएं खोजें...",
      "allSchemesCatalogue": "सभी सरकारी योजनाओं की सूची",
      "searchCatalogue": "योजना का नाम, कीवर्ड, श्रेणी, मंत्रालय या लाभ से खोजें..."
    },
    "ai": {
      "welcomeTitle": "नमस्ते! मैं आपका निजी स्कीम साथी AI सहायक हूँ।",
      "welcomeDesc": "मैं आपकी प्रोफ़ाइल, अनुपलब्ध दस्तावेज़ों और पात्र योजनाओं से पूरी तरह अवगत हूँ। मैं केवल सत्यापित सरकारी डेटा (.gov.in) का उपयोग करता हूँ।",
      "inputPlaceholder": "अपनी पसंदीदा भाषा में सरकारी योजनाओं के बारे में प्रश्न पूछें...",
      "chip1": "मुझे कौन सी सरकारी योजनाएं मिल सकती हैं?",
      "chip2": "मुझे सबसे पहले किस योजना में आवेदन करना चाहिए?",
      "chip3": "मेरा कौन सा दस्तावेज़ बाकी है?"
    }
  },
  "mr": {
    "appTitle": "स्कीम साथी",
    "appSubtitle": "नागरिक सरकारी योजना आणि दस्तऐवज कृती मंच",
    "safetyNotice": "अधिकृत सुरक्षा सूचना: स्कीम साथी आपल्याकडून कधीही सरकारी पासवर्ड, OTP किंवा UPI PIN मागणार नाही. अनधिकृत व्यक्तींपासून सावध राहा.",
    "nav": {
      "allSchemes": "सर्व सरकारी योजना",
      "forMe": "माझ्यासाठी (पात्र)",
      "vault": "माझे दस्तऐवज",
      "applications": "माझे अर्ज",
      "compare": "तुलना करा",
      "lifeEvents": "जीवन-घटना",
      "fraudShield": "सुरक्षा कवच",
      "privacy": "माझी गोपनीयता",
      "admin": "प्रशासक नोंदवही"
    },
    "healthCheck": {
      "title": "माझी योजना आरोग्य तपासणी",
      "subtitle": "तुमच्या प्रोफाइल आणि दस्तऐवज तयारीवर आधारित थेट आरोग्य स्थिती",
      "eligible": "पात्र योजना",
      "highPriority": "उच्च प्राधान्य",
      "readyToApply": "अर्जासाठी सज्ज",
      "inProgress": "प्रक्रियेतील अर्ज",
      "missingDocs": "अपूर्ण दस्तऐवज",
      "expiringDocs": "कालबाह्य होणारे दस्तऐवज",
      "upcomingDeadlines": "आगामी अंतिम मुदती"
    },
    "nextAction": {
      "title": "माझी पुढील कृती",
      "readyNow": "आता तयार",
      "step": "टप्पा १: आवश्यक दस्तऐवज गोळा करा",
      "applyButton": "अधिकृत पोर्टलवर अर्ज करा"
    },
    "schemeCard": {
      "recommended": "शिफारस केलेली",
      "verified": "अधिकृत .gov.in",
      "benefit": "मिळणारा लाभ",
      "deadline": "अंतिम मुदत",
      "readiness": "अर्ज तयारी",
      "compare": "तुलना करा",
      "viewDetails": "तपशील पहा",
      "readinessScore": "तयारी गुण",
      "applyNow": ".gov.in वर अर्ज करा",
      "whyRecommended": "तुमच्यासाठी शिफारस का",
      "documentGap": "दस्तऐवज पडताळणी",
      "missing": "अपूर्ण"
    },
    "ui": {
      "startMyProfile": "माझे प्रोफाइल सुरू करा",
      "exploreAllSchemes": "सर्व योजना एक्सप्लोर करा",
      "findSchemesForMe": "माझ्यासाठी योजना शोधा",
      "reportMissingScheme": "सुटलेली योजना नोंदवा",
      "saveProfileRecalculate": "प्रोफाइल जतन करा आणि योजना पुन्हा तपासा",
      "filterBy": "फिल्टर करा",
      "allCategories": "सर्व श्रेणी",
      "matchingSchemes": "पात्र योजना",
      "searchPlaceholder": "पात्र योजना शोधा...",
      "allSchemesCatalogue": "सर्व सरकारी योजनांची सूची",
      "searchCatalogue": "योजनेचे नाव, श्रेणी किंवा मंत्रालयानुसार शोधा..."
    },
    "ai": {
      "welcomeTitle": "नमस्कार! मी तुमचा वैयक्तिक स्कीम साथी AI मार्गदर्शक आहे.",
      "welcomeDesc": "मी तुमच्या नागरिक प्रोफाइल आणि व्हॉल्ट दस्तऐवजांनुसार पात्र योजना शोधतो. मी केवळ अधिकृत सरकारी माहिती (.gov.in) वापरतो.",
      "inputPlaceholder": "तुमच्या पसंतीच्या भाषेत सरकारी योजनांबद्दल प्रश्न विचारा...",
      "chip1": "मला कोणत्या योजना मिळतील?",
      "chip2": "मी आधी कोणत्या योजनेसाठी अर्ज करावा?",
      "chip3": "माझे कोणते कागदपत्र अपूर्ण आहे?"
    }
  },
  "bn": {
    "appTitle": "স্কিম সাথী",
    "appSubtitle": "নাগরিক সরকারি স্কিম ও নথি সহায়তা ইঞ্জিন",
    "safetyNotice": "অফিসিয়াল নিরাপত্তা বিজ্ঞপ্তি: স্কিম সাথী কখনই আপনার সরকারি পোর্টাল পাসওয়ার্ড, ওটিপি বা ইউপিআই পিন চাইবে না।",
    "nav": {
      "allSchemes": "সমস্ত সরকারি স্কিম",
      "forMe": "আমার জন্য (যোগ্য)",
      "vault": "আমার নথিপত্র",
      "applications": "আমার আবেদন",
      "compare": "তুলনা করুন",
      "lifeEvents": "জীবনের ঘটনা",
      "fraudShield": "প্রতারণা সুরক্ষা",
      "privacy": "আমার গোপনীয়তা",
      "admin": "অ্যাডমিন রেজিস্ট্রি"
    },
    "healthCheck": {
      "title": "আমার স্কিম স্বাস্থ্য পরীক্ষা",
      "subtitle": "আপনার প্রোফাইল এবং নথির প্রস্তুতির উপর ভিত্তি করে লাইভ স্থিতি",
      "eligible": "যোগ্য স্কিম",
      "highPriority": "উচ্চ অগ্রাধিকার",
      "readyToApply": "আবেদনের জন্য প্রস্তুত",
      "inProgress": "চলমান আবেদন",
      "missingDocs": "অনুপস্থিত নথি",
      "expiringDocs": "মেয়াদোত্তীর্ণ নথি",
      "upcomingDeadlines": "আসন্ন শেষ তারিখ"
    },
    "nextAction": {
      "title": "আমার পরবর্তী পদক্ষেপ",
      "readyNow": "এখন প্রস্তুত",
      "step": "ধাপ ১: প্রয়োজনীয় নথি সংগ্রহ করুন",
      "applyButton": "অফিসিয়াল পোর্টালে আবেদন করুন"
    },
    "schemeCard": {
      "recommended": "প্রস্তাবিত",
      "verified": "যাচাইকৃত .gov.in",
      "benefit": "সুবিধা",
      "deadline": "শেষ তারিখ",
      "readiness": "আবেদনের প্রস্তুতি",
      "compare": "তুলনা করুন",
      "viewDetails": "বিস্তারিত দেখুন",
      "readinessScore": "প্রস্তুতি স্কোর",
      "applyNow": ".gov.in-এ আবেদন করুন",
      "whyRecommended": "আপনার জন্য কেন প্রস্তাবিত",
      "documentGap": "নথি ঘাটতি বিশ্লেষণ",
      "missing": "অনুপস্থিত"
    },
    "ui": {
      "startMyProfile": "আমার প্রোফাইল শুরু করুন",
      "exploreAllSchemes": "সমস্ত স্কিম দেখুন",
      "findSchemesForMe": "আমার জন্য স্কিম খুঁজুন",
      "reportMissingScheme": "অনুপস্থিত স্কিম রিপোর্ট করুন",
      "saveProfileRecalculate": "প্রোফাইল সংরক্ষণ করুন এবং স্কিম পুনঃগণনা করুন",
      "filterBy": "ফিল্টার করুন",
      "allCategories": "সমস্ত বিভাগ",
      "matchingSchemes": "মেলা স্কিম",
      "searchPlaceholder": "স্কিম অনুসন্ধান করুন...",
      "allSchemesCatalogue": "সমস্ত সরকারি স্কিম ক্যাটালগ",
      "searchCatalogue": "স্কিমের নাম, বিভাগ বা সুবিধা দিয়ে খুঁজুন..."
    },
    "ai": {
      "welcomeTitle": "নমস্কার! আমি আপনার ব্যক্তিগত স্কিম সাথী AI সহকারী।",
      "welcomeDesc": "আমি আপনার প্রোফাইল এবং নথিপত্র অনুসারে সঠিক সরকারি স্কিম খুঁজতে সাহায্য করি।",
      "inputPlaceholder": "সরকারি স্কিম সম্পর্কে আপনার ভাষায় প্রশ্ন জিজ্ঞাসা করুন...",
      "chip1": "আমি কোন স্কিমগুলির জন্য যোগ্য?",
      "chip2": "আমার প্রথমে কোন স্কিমের জন্য আবেদন করা উচিত?",
      "chip3": "আমার কোন নথি অনুপস্থিত?"
    }
  },
  "gu": {
    "appTitle": "સ્કીમ સાથી",
    "appSubtitle": "નાગરિક સરકારી યોજના અને દસ્તાવેજ સહાયક એન્જિન",
    "safetyNotice": "સત્તાવાર સુરક્ષા સૂચના: સ્કીમ સાથી ક્યારેય તમારો પાસવર્ડ, OTP કે UPI PIN માંગશે નહીં.",
    "nav": {
      "allSchemes": "બધી સરકારી યોજનાઓ",
      "forMe": "મારા માટે (પાત્ર)",
      "vault": "મારા દસ્તાવેજો",
      "applications": "મારી અરજીઓ",
      "compare": "સરખામણી કરો",
      "lifeEvents": "જીવનની ઘટનાઓ",
      "fraudShield": "છેતરપિંડી સુરક્ષા",
      "privacy": "મારી ગોપનીયતા",
      "admin": "એડમિન રજિસ્ટ્રી"
    },
    "healthCheck": {
      "title": "મારી યોજના આરોગ્ય તપાસ",
      "subtitle": "તમારી પ્રોફાઇલ અને દસ્તાવેજ સજ્જતા પર આધારિત સ્થિતિ",
      "eligible": "પાત્ર યોજનાઓ",
      "highPriority": "ઉચ્ચ અગ્રતા",
      "readyToApply": "અરજી કરવા માટે તૈયાર",
      "inProgress": "ચાલુ અરજીઓ",
      "missingDocs": "ખૂટતા દસ્તાવેજો",
      "expiringDocs": "મુદત પૂરી થતા દસ્તાવેજો",
      "upcomingDeadlines": "આગામી અંતિમ તારીખો"
    },
    "nextAction": {
      "title": "મારું આગલું પગલું",
      "readyNow": "હમણાં તૈયાર",
      "step": "પગલું ૧: જરૂરી દસ્તાવેજો એકત્ર કરો",
      "applyButton": "સત્તાવાર પોર્ટલ પર અરજી કરો"
    },
    "schemeCard": {
      "recommended": "ભલામણ કરેલ",
      "verified": "ચકાસાયેલ .gov.in",
      "benefit": "લાભ",
      "deadline": "છેલ્લી તારીખ",
      "readiness": "અરજી સજ્જતા",
      "compare": "સરખામણી કરો",
      "viewDetails": "વિગતો જુઓ",
      "readinessScore": "સજ્જતા સ્કોર",
      "applyNow": ".gov.in પર અરજી કરો",
      "whyRecommended": "તમારા માટે ભલામણ કેમ",
      "documentGap": "દસ્તાવેજ અંતર વિશ્લેષણ",
      "missing": "ખૂટે છે"
    },
    "ui": {
      "startMyProfile": "મારી પ્રોફાઇલ શરૂ કરો",
      "exploreAllSchemes": "બધી યોજનાઓ જુઓ",
      "findSchemesForMe": "મારા માટે યોજનાઓ શોધો",
      "reportMissingScheme": "ખૂટતી યોજનાની જાણ કરો",
      "saveProfileRecalculate": "પ્રોફાઇલ સાચવો અને યોજનાઓ ફરી ગણો",
      "filterBy": "ફિલ્ટર કરો",
      "allCategories": "બધી શ્રેણીઓ",
      "matchingSchemes": "સુસંગત યોજનાઓ",
      "searchPlaceholder": "યોજનાઓ શોધો...",
      "allSchemesCatalogue": "બધી સરકારી યોજનાઓની સૂચિ",
      "searchCatalogue": "યોજનાનું નામ, કેટેગરી કે લાભ દ્વારા શોધો..."
    },
    "ai": {
      "welcomeTitle": "નમસ્તે! હું તમારો વ્યક્તિગત સ્કીમ સાથી AI સહાયક છું.",
      "welcomeDesc": "હું તમારી પ્રોફાઇલ અને દસ્તાવેજો અનુસાર સત્તાવાર સરકારી યોજનાઓ શોધવામાં મદદ કરું છું.",
      "inputPlaceholder": "તમારી પસંદગીની ભાષામાં સરકારી યોજનાઓ વિશે પૂછો...",
      "chip1": "હું કઈ યોજનાઓ માટે પાત્ર છું?",
      "chip2": "મારે પહેલા કઈ યોજના માટે અરજી કરવી જોઈએ?",
      "chip3": "મારો કયો દસ્તાવેજ ખૂટે છે?"
    }
  },
  "ta": {
    "appTitle": "ஸ்கீம் சாதி",
    "appSubtitle": "குடிமக்கள் அரசுத் திட்டங்கள் மற்றும் ஆவண வழிகாட்டி",
    "safetyNotice": "அதிகாரப்பூர்வ பாதுகாப்பு அறிவிப்பு: ஸ்கீம் சாதி ஒருபோதும் உங்கள் கடவுச்சொல், OTP அல்லது UPI PIN ஐக் கேட்காது.",
    "nav": {
      "allSchemes": "அனைத்து அரசுத் திட்டங்கள்",
      "forMe": "எனக்கானவை (தகுதியானவை)",
      "vault": "எனது ஆவணங்கள்",
      "applications": "எனது விண்ணப்பங்கள்",
      "compare": "ஒப்பிடுக",
      "lifeEvents": "வாழ்க்கை நிகழ்வுகள்",
      "fraudShield": "மோசடி தடுப்பு",
      "privacy": "எனது தனியுரிமை",
      "admin": "நிர்வாகப் பதிவேடு"
    },
    "healthCheck": {
      "title": "எனது திட்ட சுகாதார சோதனை",
      "subtitle": "உங்கள் சுயவிவரம் மற்றும் ஆவணத் தயார்நிலை அடிப்படையிலான நேரடி நிலை",
      "eligible": "தகுதியான திட்டங்கள்",
      "highPriority": "உயர் முன்னுரிமை",
      "readyToApply": "விண்ணப்பிக்க தயார்",
      "inProgress": "செயலில் உள்ள விண்ணப்பங்கள்",
      "missingDocs": "விடுபட்ட ஆவணங்கள்",
      "expiringDocs": "காலாவதியாகும் ஆவணங்கள்",
      "upcomingDeadlines": "வரவிருக்கும் கடைசி தேதிகள்"
    },
    "nextAction": {
      "title": "எனது அடுத்த நடவடிக்கை",
      "readyNow": "இப்போது தயார்",
      "step": "படி 1: தேவையான ஆவணங்களைச் சேகரிக்கவும்",
      "applyButton": "அதிகாரப்பூர்வ தளத்தில் விண்ணப்பிக்கவும்"
    },
    "schemeCard": {
      "recommended": "பரிந்துரைக்கப்பட்டது",
      "verified": "சரிபார்க்கப்பட்டது .gov.in",
      "benefit": "பயன்",
      "deadline": "கடைசி தேதி",
      "readiness": "விண்ணப்பத் தயார்நிலை",
      "compare": "ஒப்பிடுக",
      "viewDetails": "விவரங்களைக் காண்க",
      "readinessScore": "தயார்நிலை மதிப்பெண்",
      "applyNow": ".gov.in இல் விண்ணப்பிக்கவும்",
      "whyRecommended": "உங்களுக்கு ஏன் பரிந்துரைக்கப்பட்டது",
      "documentGap": "ஆவண இடைவெளி பகுப்பாய்வு",
      "missing": "விடுபட்டது"
    },
    "ui": {
      "startMyProfile": "சுயவிவரத்தைத் தொடங்கவும்",
      "exploreAllSchemes": "அனைத்துத் திட்டங்களையும் காண்க",
      "findSchemesForMe": "எனக்கான திட்டங்களைக் கண்டறியவும்",
      "reportMissingScheme": "விடுபட்ட திட்டத்தைப் புகாரளிக்கவும்",
      "saveProfileRecalculate": "சுயவிவரத்தைச் சேமித்து திட்டங்களை மீண்டும் கணக்கிடுங்கள்",
      "filterBy": "வடிகட்டு",
      "allCategories": "அனைத்துப் பிரிவுகள்",
      "matchingSchemes": "பொருந்தும் திட்டங்கள்",
      "searchPlaceholder": "திட்டங்களைத் தேடுங்கள்...",
      "allSchemesCatalogue": "அனைத்து அரசுத் திட்டங்களின் பட்டியல்",
      "searchCatalogue": "திட்டத்தின் பெயர், வகை அல்லது பயன் மூலம் தேடுங்கள்..."
    },
    "ai": {
      "welcomeTitle": "வணக்கம்! நான் உங்கள் தனிப்பட்ட ஸ்கீம் சாதி AI உதவியாளர்.",
      "welcomeDesc": "உங்கள் சுயவிவரம் மற்றும் ஆவணங்களின் அடிப்படையில் சரியான அரசுத் திட்டங்களைக் கண்டறிய நான் உதவுகிறேன்.",
      "inputPlaceholder": "உங்கள் மொழியில் அரசுத் திட்டங்கள் பற்றிக் கேளுங்கள்...",
      "chip1": "நான் எந்தத் திட்டங்களுக்குத் தகுதியானவன்?",
      "chip2": "நான் முதலில் எந்தத் திட்டத்திற்கு விண்ணப்பிக்க வேண்டும்?",
      "chip3": "என்னிடம் எந்த ஆவணம் இல்லை?"
    }
  },
  "te": {
    "appTitle": "స్కీమ్ సాథీ",
    "appSubtitle": "పౌర ప్రభుత్వ పథకాలు మరియు పత్రాల కార్యాచరణ ఇంజిన్",
    "safetyNotice": "అధికారిక భద్రతా నోటీసు: స్కీమ్ సాథీ మీ పాస్‌వర్డ్, OTP లేదా UPI PIN ఎప్పుడూ అడగదు.",
    "nav": {
      "allSchemes": "అన్ని ప్రభుత్వ పథకాలు",
      "forMe": "నా కోసం (అర్హత ఉన్నవి)",
      "vault": "నా పత్రాలు",
      "applications": "నా దరఖాస్తులు",
      "compare": "పోల్చండి",
      "lifeEvents": "జీవిత సంఘటనలు",
      "fraudShield": "మోసం రక్షణ",
      "privacy": "నా గోప్యత",
      "admin": "అడ్మిన్ రిజిస్ట్రీ"
    },
    "healthCheck": {
      "title": "నా పథకాల ఆరోగ్య తనిఖీ",
      "subtitle": "మీ ప్రొఫైల్ మరియు పత్రాల సంసిద్ధత ఆధారంగా ప్రత్యక్ష స్థితి",
      "eligible": "అర్హత గల పథకాలు",
      "highPriority": "అధిక ప్రాధాన్యత",
      "readyToApply": "దరఖాస్తుకు సిద్ధంగా ఉంది",
      "inProgress": "పురోగతిలో ఉన్న దరఖాస్తులు",
      "missingDocs": "తప్పిపోయిన పత్రాలు",
      "expiringDocs": "గడువు ముగిసే పత్రాలు",
      "upcomingDeadlines": "రాబోయే గడువు తేదీలు"
    },
    "nextAction": {
      "title": "నా తదుపరి చర్య",
      "readyNow": "ఇప్పుడు సిద్ధం",
      "step": "దశ 1: అవసరమైన పత్రాలను సేకరించండి",
      "applyButton": "అధికారిక పోర్టల్‌లో దరఖాస్తు చేసుకోండి"
    },
    "schemeCard": {
      "recommended": "సిఫార్సు చేయబడింది",
      "verified": "ధృవీకరించబడింది .gov.in",
      "benefit": "ప్రయోజనం",
      "deadline": "చివరి తేదీ",
      "readiness": "దరఖాస్తు సంసిద్ధత",
      "compare": "పోల్చండి",
      "viewDetails": "వివరాలు చూడండి",
      "readinessScore": "సంసిద్ధత స్కోరు",
      "applyNow": ".gov.in లో దరఖాస్తు చేయండి",
      "whyRecommended": "మీకు ఎందుకు సిఫార్సు చేయబడింది",
      "documentGap": "పత్రాల విశ్లేషణ",
      "missing": "తప్పిపోయింది"
    },
    "ui": {
      "startMyProfile": "నా ప్రొఫైల్ ప్రారంభించండి",
      "exploreAllSchemes": "అన్ని పథకాలను అన్వేషించండి",
      "findSchemesForMe": "నా కోసం పథకాలను కనుగొనండి",
      "reportMissingScheme": "తప్పిపోయిన పథకాన్ని నివేదించండి",
      "saveProfileRecalculate": "ప్రొఫైల్ సేవ్ చేసి పథకాలను తిరిగి లెక్కించండి",
      "filterBy": "ఫిల్టర్ చేయండి",
      "allCategories": "అన్ని వర్గాలు",
      "matchingSchemes": "సరిపోలే పథకాలు",
      "searchPlaceholder": "పథకాలను శోధించండి...",
      "allSchemesCatalogue": "అన్ని ప్రభుత్వ పథకాల జాబితా",
      "searchCatalogue": "పథకం పేరు, వర్గం లేదా ప్రయోజనం ద్వారా శోధించండి..."
    },
    "ai": {
      "welcomeTitle": "నమస్కారం! నేను మీ వ్యక్తిగత స్కీమ్ సాథీ AI సహాయకుడిని.",
      "welcomeDesc": "మీ ప్రొఫైల్ ఆధారంగా ధృవీకరించబడిన ప్రభుత్వ పథకాల వివరాలను నేను అందిస్తాను.",
      "inputPlaceholder": "మీ ప్రాధాన్యత భాషలో ప్రభుత్వ పథకాల గురించి అడగండి...",
      "chip1": "నేను ఏ పథకాలకు అర్హుడిని?",
      "chip2": "నేను మొదట ఏ పథకానికి దరఖాస్తు చేసుకోవాలి?",
      "chip3": "నా దగ్గర ఏ పత్రం లేదు?"
    }
  },
  "kn": {
    "appTitle": "ಸ್ಕೀಮ್ ಸಾಥಿ",
    "appSubtitle": "ನಾಗರಿಕ ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು ಮತ್ತು ದಾಖಲೆಗಳ ವೇದಿಕೆ",
    "safetyNotice": "ಅಧಿಕೃತ ಭದ್ರತಾ ಸೂಚನೆ: ಸ್ಕೀಮ್ ಸಾಥಿ ನಿಮ್ಮ ಪಾಸ್‌ವರ್ಡ್, OTP ಅಥವಾ UPI PIN ಅನ್ನು ಎಂದಿಗೂ ಕೇಳುವುದಿಲ್ಲ.",
    "nav": {
      "allSchemes": "ಎಲ್ಲಾ ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು",
      "forMe": "ನನಗಾಗಿ (ಅರ್ಹ)",
      "vault": "ನನ್ನ ದಾಖಲೆಗಳು",
      "applications": "ನನ್ನ ಅರ್ಜಿಗಳು",
      "compare": "ಹೋಲಿಕೆ ಮಾಡಿ",
      "lifeEvents": "ಜೀವನ ಘಟನೆಗಳು",
      "fraudShield": "ವಂಚನೆ ರಕ್ಷಣೆ",
      "privacy": "ನನ್ನ ಗೌಪ್ಯತೆ",
      "admin": "ನಿರ್ವಾಹಕ ನೋಂದಣಿ"
    },
    "healthCheck": {
      "title": "ನನ್ನ ಯೋಜನೆ ಆರೋಗ್ಯ ತಪಾಸಣೆ",
      "subtitle": "ನಿಮ್ಮ ಪ್ರೊಫೈಲ್ ಮತ್ತು ದಾಖಲೆಗಳ ಸಿದ್ಧತೆಯ ಆಧಾರದ ಸ್ಥಿತಿ",
      "eligible": "ಅರ್ಹ ಯೋಜನೆಗಳು",
      "highPriority": "ಹೆಚ್ಚಿನ ಆದ್ಯತೆ",
      "readyToApply": "ಅರ್ಜಿ ಸಲ್ಲಿಸಲು ಸಿದ್ಧ",
      "inProgress": "ಪ್ರಗತಿಯಲ್ಲಿರುವ ಅರ್ಜಿಗಳು",
      "missingDocs": "ಕಾಣೆಯಾದ ದಾಖಲೆಗಳು",
      "expiringDocs": "ಅವಧಿ ಮುಗಿಯುವ ದಾಖಲೆಗಳು",
      "upcomingDeadlines": "ಮುಂಬರುವ ಕೊನೆಯ ದಿನಾಂಕಗಳು"
    },
    "nextAction": {
      "title": "ನನ್ನ ಮುಂದಿನ ಕ್ರಮ",
      "readyNow": "ಈಗ ಸಿದ್ಧ",
      "step": "ಹಂತ 1: ಅಗತ್ಯ ದಾಖಲೆಗಳನ್ನು ಸಂಗ್ರಹಿಸಿ",
      "applyButton": "ಅಧಿಕೃತ ಪೋರ್ಟಲ್‌ನಲ್ಲಿ ಅರ್ಜಿ ಸಲ್ಲಿಸಿ"
    },
    "schemeCard": {
      "recommended": "ಶಿಫಾರಸು ಮಾಡಲಾಗಿದೆ",
      "verified": "ಪರಿಶೀಲಿಸಲಾಗಿದೆ .gov.in",
      "benefit": "ಪ್ರಯೋಜನ",
      "deadline": "ಕೊನೆಯ ದಿನಾಂಕ",
      "readiness": "ಅರ್ಜಿ ಸಿದ್ಧತೆ",
      "compare": "ಹೋಲಿಕೆ ಮಾಡಿ",
      "viewDetails": "ವಿವರಗಳನ್ನು ವೀಕ್ಷಿಸಿ",
      "readinessScore": "ಸಿದ್ಧತೆ ಸ್ಕೋರ್",
      "applyNow": ".gov.in ನಲ್ಲಿ ಅರ್ಜಿ ಸಲ್ಲಿಸಿ",
      "whyRecommended": "ನಿಮಗೆ ಏಕೆ ಶಿಫಾರಸು ಮಾಡಲಾಗಿದೆ",
      "documentGap": "ದಾಖಲೆಗಳ ವಿಶ್ಲೇಷಣೆ",
      "missing": "ಕಾಣೆಯಾಗಿದೆ"
    },
    "ui": {
      "startMyProfile": "ನನ್ನ ಪ್ರೊಫೈಲ್ ಪ್ರಾರಂಭಿಸಿ",
      "exploreAllSchemes": "ಎಲ್ಲಾ ಯೋಜನೆಗಳನ್ನು ಅನ್ವೇಷಿಸಿ",
      "findSchemesForMe": "ನನಗಾಗಿ ಯೋಜನೆಗಳನ್ನು ಹುಡುಕಿ",
      "reportMissingScheme": "ಕಾಣೆಯಾದ ಯೋಜನೆಯನ್ನು ವರದಿ ಮಾಡಿ",
      "saveProfileRecalculate": "ಪ್ರೊಫೈಲ್ ಉಳಿಸಿ ಮತ್ತು ಯೋಜನೆಗಳನ್ನು ಮರು ಲೆಕ್ಕಾಚಾರ ಮಾಡಿ",
      "filterBy": "ಫಿಲ್ಟರ್ ಮಾಡಿ",
      "allCategories": "ಎಲ್ಲಾ ವರ್ಗಗಳು",
      "matchingSchemes": "ಹೊಂದಾಣಿಕೆಯ ಯೋಜನೆಗಳು",
      "searchPlaceholder": "ಯೋಜನೆಗಳನ್ನು ಹುಡುಕಿ...",
      "allSchemesCatalogue": "ಎಲ್ಲಾ ಸರ್ಕಾರಿ ಯೋಜನೆಗಳ ಕ್ಯಾಟಲಾಗ್",
      "searchCatalogue": "ಯೋಜನೆಯ ಹೆಸರು, ವರ್ಗ ಅಥವಾ ಪ್ರಯೋಜನದ ಮೂಲಕ ಹುಡುಕಿ..."
    },
    "ai": {
      "welcomeTitle": "ನಮಸ್ಕಾರ! ನಾನು ನಿಮ್ಮ ವೈಯಕ್ತಿಕ ಸ್ಕೀಮ್ ಸಾಥಿ AI ಸಹಾಯಕ.",
      "welcomeDesc": "ನಿಮ್ಮ ಪ್ರೊಫೈಲ್ ಆಧಾರದ ಮೇಲೆ ಅರ್ಹ ಸರ್ಕಾರಿ ಯೋಜನೆಗಳನ್ನು ಹುಡುಕಲು ನಾನು ಸಹಾಯ ಮಾಡುತ್ತೇನೆ.",
      "inputPlaceholder": "ನಿಮ್ಮ ಭಾಷೆಯಲ್ಲಿ ಸರ್ಕಾರಿ ಯೋಜನೆಗಳ ಬಗ್ಗೆ ಪ್ರಶ್ನೆ ಕೇಳಿ...",
      "chip1": "ನಾನು ಯಾವ ಯೋಜನೆಗಳಿಗೆ ಅರ್ಹನಾಗಿದ್ದೇನೆ?",
      "chip2": "ನಾನು ಮೊದಲು ಯಾವ ಯೋಜನೆಗೆ ಅರ್ಜಿ ಸಲ್ಲಿಸಬೇಕು?",
      "chip3": "ನನ್ನ ಯಾವ ದಾಖಲೆ ಕಾಣೆಯಾಗಿದೆ?"
    }
  },
  "ml": {
    "appTitle": "സ്കീം സാഥി",
    "appSubtitle": "പൗര സർക്കാർ പദ്ധതികളും രേഖകളും സഹായ എഞ്ചിൻ",
    "safetyNotice": "ഔദ്യോഗിക സുരക്ഷാ അറിയിപ്പ്: സ്കീം സാഥി ഒരിക്കലും നിങ്ങളുടെ പാസ്‌വേഡ്, OTP അല്ലെങ്കിൽ UPI PIN ചോദിക്കില്ല.",
    "nav": {
      "allSchemes": "എല്ലാ സർക്കാർ പദ്ധതികളും",
      "forMe": "എനിക്കായി (അർഹമായവ)",
      "vault": "എന്റെ രേഖകൾ",
      "applications": "എന്റെ അപേക്ഷകൾ",
      "compare": "താരതമ്യം ചെയ്യുക",
      "lifeEvents": "ജീവിത സംഭവങ്ങൾ",
      "fraudShield": "തട്ടിപ്പ് പ്രതിരോധം",
      "privacy": "എന്റെ സ്വകാര്യത",
      "admin": "അഡ്മിൻ രജിസ്ട്രി"
    },
    "healthCheck": {
      "title": "എന്റെ പദ്ധതി ആരോഗ്യ പരിശോധന",
      "subtitle": "നിങ്ങളുടെ പ്രൊഫൈലും രേഖകളും അടിസ്ഥാനമാക്കിയുള്ള തത്സമയ നില",
      "eligible": "അർഹമായ പദ്ധതികൾ",
      "highPriority": "ഉയർന്ന മുൻഗണന",
      "readyToApply": "അപേക്ഷിക്കാൻ തയ്യാറാണ്",
      "inProgress": "പുരോഗതിയിലുള്ള അപേക്ഷകൾ",
      "missingDocs": "ലഭ്യമല്ലാത്ത രേഖകൾ",
      "expiringDocs": "കാലഹരണപ്പെടുന്ന രേഖകൾ",
      "upcomingDeadlines": "വരാനിരിക്കുന്ന അവസാന തീയതികൾ"
    },
    "nextAction": {
      "title": "എന്റെ അടുത്ത നടപടി",
      "readyNow": "ഇപ്പോൾ തയ്യാറാണ്",
      "step": "ഘട്ടം 1: ആവശ്യമായ രേഖകൾ ശേഖരിക്കുക",
      "applyButton": "ഔദ്യോഗിക പോർട്ടലിൽ അപേക്ഷിക്കുക"
    },
    "schemeCard": {
      "recommended": "ശുപാർശ ചെയ്യുന്നത്",
      "verified": "സ്ഥിരീകരിച്ചത് .gov.in",
      "benefit": "ആനുകൂല്യം",
      "deadline": "അവസാന തീയതി",
      "readiness": "അപേക്ഷാ സന്നദ്ധത",
      "compare": "താരതമ്യം ചെയ്യുക",
      "viewDetails": "വിശദാംശങ്ങൾ കാണുക",
      "readinessScore": "സന്നദ്ധത സ്കോർ",
      "applyNow": ".gov.in ൽ അപേക്ഷിക്കുക",
      "whyRecommended": "നിങ്ങൾക്കായി എന്ത് കൊണ്ട് ശുപാർശ ചെയ്തു",
      "documentGap": "രേഖകളുടെ വിശകലനം",
      "missing": "ലഭ്യമല്ല"
    },
    "ui": {
      "startMyProfile": "എന്റെ പ്രൊഫൈൽ ആരംഭിക്കുക",
      "exploreAllSchemes": "എല്ലാ പദ്ധതികളും കാണുക",
      "findSchemesForMe": "എനിക്കായുള്ള പദ്ധതികൾ കണ്ടെത്തുക",
      "reportMissingScheme": "വിട്ടുപോയ പദ്ധതി റിപ്പോർട്ട് ചെയ്യുക",
      "saveProfileRecalculate": "പ്രൊഫൈൽ സംരക്ഷിച്ച് പദ്ധതികൾ വീണ്ടും കണക്കാക്കുക",
      "filterBy": "ഫിൽട്ടർ ചെയ്യുക",
      "allCategories": "എല്ലാ വിഭാഗങ്ങളും",
      "matchingSchemes": "അനുയോജ്യമായ പദ്ധതികൾ",
      "searchPlaceholder": "പദ്ധതികൾ തിരയുക...",
      "allSchemesCatalogue": "എല്ലാ സർക്കാർ പദ്ധതികളുടെയും കാറ്റലോഗ്",
      "searchCatalogue": "പദ്ധതിയുടെ പേര്, വിഭാഗം അല്ലെങ്കിൽ ആനുകൂല്യം വഴി തിരയുക..."
    },
    "ai": {
      "welcomeTitle": "നമസ്കാരം! ഞാൻ നിങ്ങളുടെ വ്യക്തിഗത സ്കീം സാഥി AI സഹായിയാണ്.",
      "welcomeDesc": "നിങ്ങളുടെ പ്രൊഫൈൽ അടിസ്ഥാനമാക്കി ഔദ്യോഗിക സർക്കാർ പദ്ധതികൾ കണ്ടെത്താൻ ഞാൻ സഹായിക്കുന്നു.",
      "inputPlaceholder": "നിങ്ങളുടെ ഭാഷയിൽ സർക്കാർ പദ്ധതികളെക്കുറിച്ച് ചോദിക്കുക...",
      "chip1": "ഞാൻ ഏതൊക്കെ പദ്ധതികൾക്ക് അർഹനാണ്?",
      "chip2": "ഞാൻ ആദ്യം ഏത് പദ്ധതിക്കാണ് അപേക്ഷിക്കേണ്ടത്?",
      "chip3": "എനിക്ക് ഏത് രേഖയാണ് ഇല്ലാത്തത്?"
    }
  },
  "pa": {
    "appTitle": "ਸਕੀਮ ਸਾਥੀ",
    "appSubtitle": "ਨਾਗਰਿਕ ਸਰਕਾਰੀ ਸਕੀਮਾਂ ਅਤੇ ਦਸਤਾਵੇਜ਼ ਸਹਾਇਤਾ ਇੰਜਣ",
    "safetyNotice": "ਅਧਿਕਾਰਤ ਸੁਰੱਖਿਆ ਨੋਟਿਸ: ਸਕੀਮ ਸਾਥੀ ਕਦੇ ਵੀ ਤੁਹਾਡਾ ਪਾਸਵਰਡ, OTP ਜਾਂ UPI PIN ਨਹੀਂ ਮੰਗੇਗਾ।",
    "nav": {
      "allSchemes": "ਸਾਰੀਆਂ ਸਰਕਾਰੀ ਸਕੀਮਾਂ",
      "forMe": "ਮੇਰੇ ਲਈ (ਯੋਗ)",
      "vault": "ਮੇਰੇ ਦਸਤਾਵੇਜ਼",
      "applications": "ਮੇਰੀਆਂ ਅਰਜ਼ੀਆਂ",
      "compare": "ਤੁਲਨਾ ਕਰੋ",
      "lifeEvents": "ਜੀਵਨ ਘਟਨਾਵਾਂ",
      "fraudShield": "ਧੋਖਾਧੜੀ ਸੁਰੱਖਿਆ",
      "privacy": "ਮੇਰੀ ਗੋਪਨੀਯਤਾ",
      "admin": "ਐਡਮਿਨ ਰਜਿਸਟਰੀ"
    },
    "healthCheck": {
      "title": "ਮੇਰੀ ਸਕੀਮ ਸਿਹਤ ਜਾਂਚ",
      "subtitle": "ਤੁਹਾਡੀ ਪ੍ਰੋਫਾਈਲ ਅਤੇ ਦਸਤਾਵੇਜ਼ਾਂ ਦੀ ਤਿਆਰੀ 'ਤੇ ਆਧਾਰਿਤ ਲਾਈਵ ਸਥਿਤੀ",
      "eligible": "ਯੋਗ ਸਕੀਮਾਂ",
      "highPriority": "ਉੱਚ ਤਰਜੀਹ",
      "readyToApply": "ਅਰਜ਼ੀ ਲਈ ਤਿਆਰ",
      "inProgress": "ਪ੍ਰਕਿਰਿਆ ਅਧੀਨ ਅਰਜ਼ੀਆਂ",
      "missingDocs": "ਗੁੰਮ ਦਸਤਾਵੇਜ਼",
      "expiringDocs": "ਮਿਆਦ ਪੁੱਗਣ ਵਾਲੇ ਦਸਤਾਵੇਜ਼",
      "upcomingDeadlines": "ਆਗਾਮੀ ਆਖਰੀ ਤਾਰੀਖਾਂ"
    },
    "nextAction": {
      "title": "ਮੇਰਾ ਅਗਲਾ ਕਦਮ",
      "readyNow": "ਹੁਣੇ ਤਿਆਰ",
      "step": "ਕਦਮ 1: ਲੋੜੀਂਦੇ ਦਸਤਾਵੇਜ਼ ਇਕੱਠੇ ਕਰੋ",
      "applyButton": "ਅਧਿਕਾਰਤ ਪੋਰਟਲ 'ਤੇ ਅਰਜ਼ੀ ਦਿਓ"
    },
    "schemeCard": {
      "recommended": "ਸਿਫਾਰਸ਼ ਕੀਤੀ",
      "verified": "ਪ੍ਰਮਾਣਿਤ .gov.in",
      "benefit": "ਲਾਭ",
      "deadline": "ਆਖਰੀ ਮਿਤੀ",
      "readiness": "ਅਰਜ਼ੀ ਤਿਆਰੀ",
      "compare": "ਤੁਲਨਾ ਕਰੋ",
      "viewDetails": "ਵੇਰਵੇ ਦੇਖੋ",
      "readinessScore": "ਤਿਆਰੀ ਸਕੋਰ",
      "applyNow": ".gov.in 'ਤੇ ਅਰਜ਼ੀ ਦਿਓ",
      "whyRecommended": "ਤੁਹਾਡੇ ਲਈ ਕਿਉਂ ਸਿਫਾਰਸ਼ ਕੀਤੀ ਗਈ",
      "documentGap": "ਦਸਤਾਵੇਜ਼ ਵਿਸ਼ਲੇਸ਼ਣ",
      "missing": "ਗੁੰਮ ਹੈ"
    },
    "ui": {
      "startMyProfile": "ਮੇਰੀ ਪ੍ਰੋਫਾਈਲ ਸ਼ੁਰੂ ਕਰੋ",
      "exploreAllSchemes": "ਸਾਰੀਆਂ ਸਕੀਮਾਂ ਦੇਖੋ",
      "findSchemesForMe": "ਮੇਰੇ ਲਈ ਸਕੀਮਾਂ ਲੱਭੋ",
      "reportMissingScheme": "ਗੁੰਮ ਸਕੀਮ ਦੀ ਰਿਪੋਰਟ ਕਰੋ",
      "saveProfileRecalculate": "ਪ੍ਰੋਫਾਈਲ ਸੰਭਾਲੋ ਅਤੇ ਸਕੀਮਾਂ ਦੀ ਮੁੜ ਗਣਨਾ ਕਰੋ",
      "filterBy": "ਫਿਲਟਰ ਕਰੋ",
      "allCategories": "ਸਾਰੀਆਂ ਸ਼੍ਰੇਣੀਆਂ",
      "matchingSchemes": "ਮੇਲ ਖਾਂਦੀਆਂ ਸਕੀਮਾਂ",
      "searchPlaceholder": "ਸਕੀਮਾਂ ਖੋਜੋ...",
      "allSchemesCatalogue": "ਸਾਰੀਆਂ ਸਰਕਾਰੀ ਸਕੀਮਾਂ ਦੀ ਸੂਚੀ",
      "searchCatalogue": "ਸਕੀਮ ਦਾ ਨਾਮ, ਸ਼੍ਰੇਣੀ ਜਾਂ ਲਾਭ ਦੁਆਰਾ ਖੋਜੋ..."
    },
    "ai": {
      "welcomeTitle": "ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ! ਮੈਂ ਤੁਹਾਡਾ ਨਿੱਜੀ ਸਕੀਮ ਸਾਥੀ AI ਸਹਾਇਕ ਹਾਂ।",
      "welcomeDesc": "ਮੈਂ ਤੁਹਾਡੀ ਪ੍ਰੋਫਾਈਲ ਦੇ ਆਧਾਰ 'ਤੇ ਸਰਕਾਰੀ ਸਕੀਮਾਂ ਲੱਭਣ ਵਿੱਚ ਮਦਦ ਕਰਦਾ ਹਾਂ।",
      "inputPlaceholder": "ਆਪਣੀ ਭਾਸ਼ਾ ਵਿੱਚ ਸਰਕਾਰੀ ਸਕੀਮਾਂ ਬਾਰੇ ਪੁੱਛੋ...",
      "chip1": "ਮੈਂ ਕਿਹੜੀਆਂ ਸਕੀਮਾਂ ਲਈ ਯੋਗ ਹਾਂ?",
      "chip2": "ਮੈਨੂੰ ਪਹਿਲਾਂ ਕਿਸ ਸਕੀਮ ਲਈ ਅਰਜ਼ੀ ਦੇਣੀ ਚਾਹੀਦੀ ਹੈ?",
      "chip3": "ਮੇਰਾ ਕਿਹੜਾ ਦਸਤਾਵੇਜ਼ ਬਾਕੀ ਹੈ?"
    }
  },
  "or": {
    "appTitle": "ସ୍କିମ୍ ସାଥୀ",
    "appSubtitle": "ନାଗରିକ ସରକାରୀ ଯୋଜନା ଓ ଦଲିଲ ସହାୟତା ଇଞ୍ଜିନ୍",
    "safetyNotice": "ସରକାରୀ ସୁରକ୍ଷା ବିଜ୍ଞପ୍ତି: ସ୍କିମ୍ ସାଥୀ କେବେ ବି ଆପଣଙ୍କ ପାସୱାର୍ଡ, OTP କିମ୍ବା UPI PIN ମାଗିବ ନାହିଁ।",
    "nav": {
      "allSchemes": "ସମସ୍ତ ସରକାରୀ ଯୋଜନା",
      "forMe": "ମୋ ପାଇଁ (ଯୋଗ୍ୟ)",
      "vault": "ମୋର ଦଲିଲ",
      "applications": "ମୋର ଆବେଦନ",
      "compare": "ତୁଳନା କରନ୍ତୁ",
      "lifeEvents": "ଜୀବନ ଘଟଣା",
      "fraudShield": "ଠକେଇ ସୁରକ୍ଷା",
      "privacy": "ମୋର ଗୋପନୀୟତା",
      "admin": "ପ୍ରଶାସକ ପଞ୍ଜିକା"
    },
    "healthCheck": {
      "title": "ମୋ ଯୋଜନା ସ୍ୱାସ୍ଥ୍ୟ ଯାଞ୍ଚ",
      "subtitle": "ଆପଣଙ୍କ ପ୍ରୋଫାଇଲ୍ ଏବଂ ଦଲିଲ ପ୍ରସ୍ତୁତି ଆଧାରିତ ସ୍ଥିତି",
      "eligible": "ଯୋଗ୍ୟ ଯୋଜନା",
      "highPriority": "ଉଚ୍ଚ ପ୍ରାଥମିକତା",
      "readyToApply": "ଆବେଦନ ପାଇଁ ପ୍ରସ୍ତୁତ",
      "inProgress": "ପ୍ରକ୍ରିୟାଧୀନ ଆବେଦନ",
      "missingDocs": "ଅନୁପଲବ୍ଧ ଦଲିଲ",
      "expiringDocs": "ଅବଧି ସରିବାକୁ ଥିବା ଦଲିଲ",
      "upcomingDeadlines": "ଆଗାମୀ ଶେଷ ତାରିଖ"
    },
    "nextAction": {
      "title": "ମୋର ପରବର୍ତ୍ତୀ ପଦକ୍ଷେପ",
      "readyNow": "ବର୍ତ୍ତମାନ ପ୍ରସ୍ତୁତ",
      "step": "ପଦକ୍ଷେପ ୧: ଆବଶ୍ୟକୀୟ ଦଲିଲ ସଂଗ୍ରହ କରନ୍ତୁ",
      "applyButton": "ଅଫିସିଆଲ୍ ପୋର୍ଟାଲରେ ଆବେଦନ କରନ୍ତୁ"
    },
    "schemeCard": {
      "recommended": "ସୁପାରିଶ କରାଯାଇଛି",
      "verified": "ଯାଞ୍ଚ ହୋଇଛି .gov.in",
      "benefit": "ଲାଭ",
      "deadline": "ଶେଷ ତାରିଖ",
      "readiness": "ଆବେଦନ ପ୍ରସ୍ତୁତି",
      "compare": "ତୁଳନା କରନ୍ତୁ",
      "viewDetails": "ବିବରଣୀ ଦେଖନ୍ତୁ",
      "readinessScore": "ପ୍ରସ୍ତୁତି ସ୍କୋର",
      "applyNow": ".gov.in ରେ ଆବେଦନ କରନ୍ତୁ",
      "whyRecommended": "ଆପଣଙ୍କ ପାଇଁ କାହିଁକି ସୁପାରିଶ",
      "documentGap": "ଦଲିଲ ଅନ୍ତର ବିଶ୍ଳେଷଣ",
      "missing": "ଅନୁପଲବ୍ଧ"
    },
    "ui": {
      "startMyProfile": "ମୋର ପ୍ରୋଫାଇଲ୍ ଆରମ୍ଭ କରନ୍ତୁ",
      "exploreAllSchemes": "ସମସ୍ତ ଯୋଜନା ଦେଖନ୍ତୁ",
      "findSchemesForMe": "ମୋ ପାଇଁ ଯୋଜନା ଖୋଜନ୍ତୁ",
      "reportMissingScheme": "ଅନୁପଲବ୍ଧ ଯୋଜନା ରିପୋର୍ଟ କରନ୍ତୁ",
      "saveProfileRecalculate": "ପ୍ରୋଫାଇଲ୍ ସଂରକ୍ଷଣ କରନ୍ତୁ ଏବଂ ଯୋଜନା ପୁନଃଗଣନା କରନ୍ତୁ",
      "filterBy": "ଫିଲ୍ଟର୍ କରନ୍ତୁ",
      "allCategories": "ସମସ୍ତ ବର୍ଗ",
      "matchingSchemes": "ମେଳ ଖାଉଥିବା ଯୋଜନା",
      "searchPlaceholder": "ଯୋଜନା ଖୋଜନ୍ତୁ...",
      "allSchemesCatalogue": "ସମସ୍ତ ସରକାରୀ ଯୋଜନା ତାଲିକା",
      "searchCatalogue": "ଯୋଜନା ନାମ, ବର୍ଗ କିମ୍ବା ଲାଭ ଦ୍ୱାରା ଖୋଜନ୍ତୁ..."
    },
    "ai": {
      "welcomeTitle": "ନମସ୍କାର! ମୁଁ ଆପଣଙ୍କ ବ୍ୟକ୍ତିଗତ ସ୍କିମ୍ ସାଥୀ AI ସହାୟକ।",
      "welcomeDesc": "ମୁଁ ଆପଣଙ୍କ ପ୍ରୋଫାଇଲ୍ ଆଧାରରେ ଯୋଗ୍ୟ ସରକାରୀ ଯୋଜନା ଖୋଜିବାରେ ସାହାଯ୍ୟ କରେ।",
      "inputPlaceholder": "ଆପଣଙ୍କ ଭାଷାରେ ସରକାରୀ ଯୋଜନା ବିଷୟରେ ପଚାରନ୍ତୁ...",
      "chip1": "ମୁଁ କେଉଁ ଯୋଜନା ପାଇଁ ଯୋଗ୍ୟ?",
      "chip2": "ମୁଁ ପ୍ରଥମେ କେଉଁ ଯୋଜନା ପାଇଁ ଆବେଦନ କରିବା ଉଚିତ୍?",
      "chip3": "ମୋର କେଉଁ ଦଲିଲ ବାକି ଅଛି?"
    }
  },
  "as": {
    "appTitle": "স্কিম সাৰথী",
    "appSubtitle": "নাগৰিক চৰকাৰী আঁচনি আৰু নথি সহায়ক ইঞ্জিন",
    "safetyNotice": "চৰকাৰী নিৰাপত্তা জাননী: স্কিম সাৰথীয়ে কেতিয়াও আপোনাৰ পাছৱৰ্ড, OTP বা UPI PIN নিবিচাৰে।",
    "nav": {
      "allSchemes": "সকলো চৰকাৰী আঁচনি",
      "forMe": "মোৰ বাবে (যোগ্য)",
      "vault": "মোৰ নথিপত্ৰ",
      "applications": "মোৰ আবেদনসমূহ",
      "compare": "তুলনা কৰক",
      "lifeEvents": "জীৱনৰ ঘটনা",
      "fraudShield": "প্ৰতাৰণা সুৰক্ষা",
      "privacy": "মোৰ গোপনীয়তা",
      "admin": "প্ৰশাসক পঞ্জীয়ন"
    },
    "healthCheck": {
      "title": "মোৰ আঁচনি স্বাস্থ্য পৰীক্ষা",
      "subtitle": "আপোনাৰ প্ৰফাইল আৰু নথিৰ প্ৰস্তুতিৰ ওপৰত ভিত্তি কৰি স্থিতি",
      "eligible": "যোগ্য আঁচনি",
      "highPriority": "উচ্চ অগ্ৰাধিকাৰ",
      "readyToApply": "আবেদন কৰিবলৈ সাজু",
      "inProgress": "চলমান আবেদন",
      "missingDocs": "অনুপস্থিত নথিপত্ৰ",
      "expiringDocs": "ম্যাদ উকলিবলগীয়া নথি",
      "upcomingDeadlines": "আসন্ন অন্তিম তাৰিখ"
    },
    "nextAction": {
      "title": "মোৰ পৰৱৰ্তী পদক্ষেপ",
      "readyNow": "এতিয়া সাজু",
      "step": "পদক্ষেপ ১: প্ৰয়োজনীয় নথি সংগ্ৰহ কৰক",
      "applyButton": "অফিচিয়েল পৰ্টেলত আবেদন কৰক"
    },
    "schemeCard": {
      "recommended": "পৰামৰ্শিত",
      "verified": "পৰীক্ষিত .gov.in",
      "benefit": "লাভ",
      "deadline": "শেষ তাৰিখ",
      "readiness": "আবেদন প্ৰস্তুতি",
      "compare": "তুলনা কৰক",
      "viewDetails": "বিৱৰণ চাওক",
      "readinessScore": "প্ৰস্তুতি স্কোৰ",
      "applyNow": ".gov.in ত আবেদন কৰক",
      "whyRecommended": "আপোনাৰ বাবে কিয় পৰামৰ্শ দিয়া হৈছে",
      "documentGap": "নথি বিশ্লেষণ",
      "missing": "অনুপস্থিত"
    },
    "ui": {
      "startMyProfile": "মোৰ প্ৰফাইল আৰম্ভ কৰক",
      "exploreAllSchemes": "সকলো আঁচনি চাওক",
      "findSchemesForMe": "মোৰ বাবে আঁচনি বিচাৰক",
      "reportMissingScheme": "অনুপস্থিত আঁচনি ৰিপৰ্ট কৰক",
      "saveProfileRecalculate": "প্ৰফাইল সংৰক্ষণ কৰক আৰু আঁচনি পুনৰ গণনা কৰক",
      "filterBy": "ফিল্টাৰ কৰক",
      "allCategories": "সকলো শ্ৰেণী",
      "matchingSchemes": "মিলা আঁচনি",
      "searchPlaceholder": "আঁচনি সন্ধান কৰক...",
      "allSchemesCatalogue": "সকলো চৰকাৰী আঁচনিৰ তালিকা",
      "searchCatalogue": "আঁচনিৰ নাম, শ্ৰেণী বা লাভৰ দ্বাৰা সন্ধান কৰক..."
    },
    "ai": {
      "welcomeTitle": "নমস্কাৰ! মই আপোনাৰ ব্যক্তিগত স্কিম সাৰথী AI সহায়ক।",
      "welcomeDesc": "মই আপোনাৰ প্ৰফাইল অনুসৰি যোগ্য চৰকাৰী আঁচনি বিচাৰি দিয়াত সহায় কৰোঁ।",
      "inputPlaceholder": "আপোনাৰ ভাষাত চৰকাৰী আঁচনিৰ বিষয়ে সোধক...",
      "chip1": "মই কোনবোৰ আঁচনিৰ বাবে যোগ্য?",
      "chip2": "মই প্ৰথমে কোনখন আঁচনিৰ বাবে আবেদন কৰা উচিত?",
      "chip3": "মোৰ কোনখন নথি বাকী আছে?"
    }
  },
  "ur": {
    "appTitle": "اسکیم ساتھی",
    "appSubtitle": "شہری سرکاری اسکیمیں اور دستاویزات ایکشن انجن",
    "safetyNotice": "سرکاری سیکیورٹی نوٹس: اسکیم ساتھی آپ سے کبھی پاس ورڈ، او ٹی پی یا یو پی آئی پن نہیں مانگے گا۔",
    "nav": {
      "allSchemes": "تمام سرکاری اسکیمیں",
      "forMe": "میرے لیے (اہل)",
      "vault": "میرے دستاویزات",
      "applications": "میری درخواستیں",
      "compare": "موازنہ کریں",
      "lifeEvents": "زندگی کے واقعات",
      "fraudShield": "فراڈ سے تحفظ",
      "privacy": "میری پرائیویسی",
      "admin": "ایڈمن رجسٹری"
    },
    "healthCheck": {
      "title": "میری اسکیم ہیلتھ چیک",
      "subtitle": "آپ کے پروفائل اور دستاویزات کی تیاری کی بنیاد پر لائیو حالت",
      "eligible": "اہل اسکیمیں",
      "highPriority": "اعلیٰ ترجیح",
      "readyToApply": "درخواست کے لیے تیار",
      "inProgress": "زیر عمل درخواستیں",
      "missingDocs": "غیر موجود دستاویزات",
      "expiringDocs": "ختم ہونے والے دستاویزات",
      "upcomingDeadlines": "آنے والی آخری تاریخیں"
    },
    "nextAction": {
      "title": "میرا اگلا قدم",
      "readyNow": "ابھی تیار",
      "step": "مرحلہ 1: ضروری دستاویزات جمع کریں",
      "applyButton": "سرکاری پورٹل پر درخواست دیں"
    },
    "schemeCard": {
      "recommended": "تجویز کردہ",
      "verified": "تصدیق شدہ .gov.in",
      "benefit": "فائدہ",
      "deadline": "آخری تاریخ",
      "readiness": "درخواست کی تیاری",
      "compare": "موازنہ کریں",
      "viewDetails": "تفصیلات دیکھیں",
      "readinessScore": "تیاری کا اسکور",
      "applyNow": ".gov.in پر درخواست دیں",
      "whyRecommended": "آپ کے لیے کیوں تجویز کیا گیا",
      "documentGap": "دستاویزات کا تجزیہ",
      "missing": "غائب"
    },
    "ui": {
      "startMyProfile": "میرا پروفائل شروع کریں",
      "exploreAllSchemes": "تمام اسکیمیں دیکھیں",
      "findSchemesForMe": "میرے لیے اسکیمیں تلاش کریں",
      "reportMissingScheme": "چھوٹی ہوئی اسکیم کی اطلاع دیں",
      "saveProfileRecalculate": "پروفائل محفوظ کریں اور اسکیموں کا دوبارہ حساب لگائیں",
      "filterBy": "فلٹر کریں",
      "allCategories": "تمام زمرے",
      "matchingSchemes": "مطابقت رکھنے والی اسکیمیں",
      "searchPlaceholder": "اسکیمیں تلاش کریں...",
      "allSchemesCatalogue": "تمام سرکاری اسکیموں کی فہرست",
      "searchCatalogue": "اسکیم کے نام، زمرے یا فائدے سے تلاش کریں..."
    },
    "ai": {
      "welcomeTitle": "سلام! میں آپ کا ذاتی اسکیم ساتھی AI معاون ہوں۔",
      "welcomeDesc": "میں آپ کے پروفائل کے مطابق تصدیق شدہ سرکاری اسکیمیں تلاش کرنے میں مدد کرتا ہوں۔",
      "inputPlaceholder": "اپنی زبان میں سرکاری اسکیموں کے بارے میں پوچھیں...",
      "chip1": "میں کن اسکیموں کے لیے اہل ہوں؟",
      "chip2": "مجھے پہلے کس اسکیم میں درخواست دینی چاہیے؟",
      "chip3": "میرا کون سا دستاویز باقی ہے؟"
    }
  },
  "sa": {
    "appTitle": "योजना साथी",
    "appSubtitle": "नागरिक सर्वकारीय योजना तथा प्रलेख सहाय्यक यन्त्रम्",
    "safetyNotice": "सर्वकारीय सुरक्षा सूचना: योजना साथी भवतां पासवर्ड, OTP अथवा UPI PIN कदापि न याचते।",
    "nav": {
      "allSchemes": "सर्वाः सर्वकारीय योजनाः",
      "forMe": "मम कृते (योग्याः)",
      "vault": "मम प्रलेखाः",
      "applications": "मम आवेदनानि",
      "compare": "तुलनां कुर्वन्तु",
      "lifeEvents": "जीवन-घटनाः",
      "fraudShield": "सुरक्षा कवचम्",
      "privacy": "मम गोपनीयता",
      "admin": "प्रशासक पञ्जिका"
    },
    "healthCheck": {
      "title": "मम योजना स्वास्थ्य परीक्षणम्",
      "subtitle": "भवतां विवरणपत्रस्य प्रलेखसज्जतायाः च आधारेण प्रत्यक्षस्थितिः",
      "eligible": "योग्याः योजनाः",
      "highPriority": "उच्च प्राथमिकता",
      "readyToApply": "आवेदनाय सज्जम्",
      "inProgress": "प्रक्रियारतानि आवेदनानि",
      "missingDocs": "अनुपलब्धाः प्रलेखाः",
      "expiringDocs": "समाप्तिं गच्छन्तः प्रलेखाः",
      "upcomingDeadlines": "आगामी अन्तिमतिथयः"
    },
    "nextAction": {
      "title": "मम अग्रिमं पदम्",
      "readyNow": "अधुना सज्जम्",
      "step": "प्रथमं पदम्: आवश्यकप्रलेखान् सङ्गृह्णन्तु",
      "applyButton": "अधिकृतजालस्थाने आवेदनं कुर्वन्तु"
    },
    "schemeCard": {
      "recommended": "अनुशंसितम्",
      "verified": "प्रमाणीकृतम् .gov.in",
      "benefit": "लाभः",
      "deadline": "अन्तिमतिथिः",
      "readiness": "आवेदन सज्जता",
      "compare": "तुलनां कुर्वन्तु",
      "viewDetails": "विवरणं पश्यन्तु",
      "readinessScore": "सज्जता अङ्काः",
      "applyNow": ".gov.in जालपुटे आवेदनं कुर्वन्तु",
      "whyRecommended": "भवतां कृते किमर्थम् अनुशंसितम्",
      "documentGap": "प्रलेख अन्तर विश्लेषणम्",
      "missing": "अनुपलब्धम्"
    },
    "ui": {
      "startMyProfile": "मम विवरणपत्रं प्रारभताम्",
      "exploreAllSchemes": "सर्वाः योजनाः पश्यन्तु",
      "findSchemesForMe": "मम कृते योजनाः अन्विष्यन्तु",
      "reportMissingScheme": "अनुपलब्धयोजनायाः सूचनां ददातु",
      "saveProfileRecalculate": "विवरणपत्रं संरक्ष्य योजनानां पुनर्गणनां कुर्वन्तु",
      "filterBy": "शोधयन्तु",
      "allCategories": "सर्वे वर्गाः",
      "matchingSchemes": "योग्याः योजनाः",
      "searchPlaceholder": "योजनाः अन्विष्यन्तु...",
      "allSchemesCatalogue": "सर्वासाम् सर्वकारीययोजनानां सूची",
      "searchCatalogue": "योजनानाम, वर्गः अथवा लाभद्वारा अन्विष्यन्तु..."
    },
    "ai": {
      "welcomeTitle": "नमस्ते! अहं भवतां व्यक्तिगत योजना साथी AI सहायकोऽस्मि।",
      "welcomeDesc": "अहं भवतां विवरणपत्रानुसारं सत्यापिताः सर्वकारीयाः योजनाः अन्वेष्टुं साहाय्यं करोमि।",
      "inputPlaceholder": "सर्वकारीययोजनानां विषये स्वभाषायां पृच्छन्तु...",
      "chip1": "अहं कासां योजनानां कृते योग्यः अस्मि?",
      "chip2": "मया प्रथमतः कस्यां योजनायाम् आवेदनं कर्तव्यम्?",
      "chip3": "मम कः प्रलेखः अनुपलब्धः अस्ति?"
    }
  },
  "kok": {
    "appTitle": "स्कीम साथी",
    "appSubtitle": "नागरिक सरकारी येवजण्यो आनी दस्तावेज मजत इंजिन",
    "safetyNotice": "अधीकृत सुरक्षा सुचोवणी: स्कीम साथी केन्नाच तुमचो पासवर्ड, OTP वा UPI PIN मागचो ना.",
    "nav": {
      "allSchemes": "सगळ्यो सरकारी येवजण्यो",
      "forMe": "म्हजे खातीर (पात्र)",
      "vault": "म्हजे दस्तावेज",
      "applications": "म्हजे अर्ज",
      "compare": "तुलना करात",
      "lifeEvents": "जिणेचे प्रसंग",
      "fraudShield": "सुरक्षा कवच",
      "privacy": "म्हजी गुप्तताय",
      "admin": "प्रशासक नोंदवही"
    },
    "healthCheck": {
      "title": "म्हजी येवजण भलायकी तपासणी",
      "subtitle": "तुमच्या प्रोफायल आनी दस्तावेज तयारीचेर आदारिल्लो थेट दर्जो",
      "eligible": "पात्र येवजण्यो",
      "highPriority": "उंच प्राधान्य",
      "readyToApply": "अर्जा खातीर तयार",
      "inProgress": "प्रक्रियेंत आशिल्ले अर्ज",
      "missingDocs": "उणे दस्तावेज",
      "expiringDocs": "मुदत सोंपपी दस्तावेज",
      "upcomingDeadlines": "फुडल्यो निमाणे तारखो"
    },
    "nextAction": {
      "title": "म्हजे फुडले पावल",
      "readyNow": "आतां तयार",
      "step": "पावल १: गरजेचे दस्तावेज एकठांय करात",
      "applyButton": "अधीकृत पोर्टलाचेर अर्ज करात"
    },
    "schemeCard": {
      "recommended": "शिफारस केल्ली",
      "verified": "तपासिल्ले .gov.in",
      "benefit": "फायदो",
      "deadline": "निमाणी तारीख",
      "readiness": "अर्ज तयारी",
      "compare": "तुलना करात",
      "viewDetails": "तपशील पळयात",
      "readinessScore": "तयारी गुण",
      "applyNow": ".gov.in चेर अर्ज करात",
      "whyRecommended": "तुमचे खातीर शिफारस कित्याक",
      "documentGap": "दस्तावेज विस्लेषण",
      "missing": "उणे"
    },
    "ui": {
      "startMyProfile": "म्हजे प्रोफायल सुरू करात",
      "exploreAllSchemes": "सगळ्यो येवजण्यो पळयात",
      "findSchemesForMe": "म्हजे खातीर येवजण्यो सोधात",
      "reportMissingScheme": "सुटिल्ली येवजण नोंदयात",
      "saveProfileRecalculate": "प्रोफायल सांबाळात आनी येवजण्यो परतून तपासात",
      "filterBy": "फिल्टर करात",
      "allCategories": "सगळे प्रकार",
      "matchingSchemes": "पात्र येवजण्यो",
      "searchPlaceholder": "येवजण्यो सोधात...",
      "allSchemesCatalogue": "सगळ्या सरकारी येवजण्यांची वळेरी",
      "searchCatalogue": "येवजणेचें नांव, प्रकार वा फायद्या प्रमाण सोधात..."
    },
    "ai": {
      "welcomeTitle": "नमस्कार! हांव तुमचो वैयक्तिक स्कीम साथी AI मार्गदर्शक.",
      "welcomeDesc": "तुमच्या प्रोफायला प्रमाण अधिकृत सरकारी येवजण्यो सोदपाक हांव मजत करतां.",
      "inputPlaceholder": "तुमच्या आवडीच्या भाशेंत सरकारी येवजण्यां विशीं विचारात...",
      "chip1": "हांव खंयच्या येवजण्यांक पात्र आसां?",
      "chip2": "हांवें पयलीं खंयचे येवजणेंत अर्ज करचो?",
      "chip3": "म्हजो खंयचो दस्तावेज उणो आसा?"
    }
  }
};

  class SchemeSaathiI18n {
    constructor() {
      this.locales = LOCALES;
      this.currentLang = localStorage.getItem('schemesaathi_lang') || 'en';
      if (!this.locales[this.currentLang]) {
        this.currentLang = 'en';
      }
    }

    _resolveKey(obj, path) {
      if (!obj || !path) return null;
      if (typeof obj[path] === 'string') return obj[path];
      const parts = path.split('.');
      let cur = obj;
      for (const p of parts) {
        if (cur && typeof cur === 'object' && cur[p] !== undefined) {
          cur = cur[p];
        } else {
          return null;
        }
      }
      return typeof cur === 'string' ? cur : null;
    }

    t(key, fallback = null) {
      if (!key) return fallback || '';
      const curDict = this.locales[this.currentLang] || this.locales.en;
      let text = this._resolveKey(curDict, key);
      if (!text && this.locales.en) {
        text = this._resolveKey(this.locales.en, key);
      }
      if (!text) {
        return fallback !== null && fallback !== undefined ? String(fallback) : String(key);
      }
      return String(text);
    }

    setLanguage(lang, triggerEvent = true) {
      if (this.locales[lang]) {
        this.currentLang = lang;
      } else {
        this.currentLang = 'en';
      }
      localStorage.setItem('schemesaathi_lang', this.currentLang);

      // Update Language Select elements
      document.querySelectorAll('#language-select, .language-selector').forEach(sel => {
        if (sel.value !== this.currentLang) {
          sel.value = this.currentLang;
        }
      });

      // Translate static DOM elements annotated with data-i18n
      this.translateDOM();

      // Update AI Copilot static text & placeholders
      this.updateAiStaticText();

      if (triggerEvent) {
        window.dispatchEvent(new CustomEvent('languageChanged', { detail: { lang: this.currentLang } }));
      }
    }

    translateDOM() {
      const elements = document.querySelectorAll('[data-i18n]');
      elements.forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (!key) return;
        const translated = this.t(key);
        if (translated) {
          if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
            if (el.hasAttribute('placeholder')) {
              el.setAttribute('placeholder', translated);
            }
          } else {
            el.textContent = translated;
          }
        }
      });
    }

    updateAiStaticText() {
      const welcomeTitle = document.getElementById('ai-welcome-title');
      const welcomeDesc = document.getElementById('ai-welcome-desc');
      const inputEl = document.getElementById('ai-input');
      const presetContainer = document.getElementById('ai-preset-chips');

      if (welcomeTitle) welcomeTitle.textContent = this.t('ai.welcomeTitle', 'Namaste! I am your personal SchemeSaathi AI Copilot.');
      if (welcomeDesc) welcomeDesc.textContent = this.t('ai.welcomeDesc', 'I am aware of your profile, missing documents, and eligible schemes. I strictly use verified official government data (.gov.in).');
      if (inputEl) inputEl.placeholder = this.t('ai.inputPlaceholder', 'Ask a question about government schemes in your preferred language...');

      const c1 = this.t('ai.chip1', 'What schemes am I eligible for?');
      const c2 = this.t('ai.chip2', 'Which scheme should I apply for first?');
      const c3 = this.t('ai.chip3', 'What document am I missing?');

      if (presetContainer) {
        presetContainer.innerHTML = `
          <button onclick="askAiPreset('${c1.replace(/'/g, "\\'")}')" class="bg-white border border-indigo-200 text-indigo-800 px-2 py-1 rounded-full font-semibold hover:bg-indigo-50 text-[11px]">${c1}</button>
          <button onclick="askAiPreset('${c2.replace(/'/g, "\\'")}')" class="bg-white border border-indigo-200 text-indigo-800 px-2 py-1 rounded-full font-semibold hover:bg-indigo-50 text-[11px]">${c2}</button>
          <button onclick="askAiPreset('${c3.replace(/'/g, "\\'")}')" class="bg-white border border-indigo-200 text-indigo-800 px-2 py-1 rounded-full font-semibold hover:bg-indigo-50 text-[11px]">${c3}</button>
        `;
      }
    }
  }

  window.i18n = new SchemeSaathiI18n();

  // Bind on DOMContentLoaded
  document.addEventListener('DOMContentLoaded', () => {
    window.i18n.setLanguage(window.i18n.currentLang, false);
  });
})(window);
