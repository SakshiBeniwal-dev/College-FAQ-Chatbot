import csv
import re
from difflib import SequenceMatcher

# ==========================================
# STEP 1: COLLEGE FAQ DATA (100 QUESTIONS)
# ==========================================

faq_data = [

# -------- ADMISSION (10) --------

("Admission", "How can I apply for admission?",
 "You can apply through the college admission portal or visit the admission office.",
 "apply admission"),

("Admission", "What documents are required for admission?",
 "You generally need 10th and 12th marks cards, transfer certificate, ID proof and photographs.",
 "documents admission"),

("Admission", "What is the admission eligibility?",
 "Eligibility depends on the course. Check the admission guidelines for specific requirements.",
 "eligibility"),

("Admission", "When does admission start?",
 "Admission dates are announced on the official college website.",
 "admission dates"),

("Admission", "Can I get direct admission?",
 "Admission procedures depend on university and college guidelines.",
 "direct admission"),

("Admission", "Is there an entrance exam?",
 "Some courses may require entrance examinations. Contact the admission department.",
 "entrance exam"),

("Admission", "How can I check my admission status?",
 "You can check your admission status through the admission portal or contact the office.",
 "admission status"),

("Admission", "Can I change my course after admission?",
 "Course changes depend on seat availability and college regulations.",
 "change course"),

("Admission", "Is there an age limit for admission?",
 "Age requirements depend on the course and applicable admission rules.",
 "age limit"),

("Admission", "Where is the admission office?",
 "Visit the college administration building to locate the admission office.",
 "admission office"),


# -------- COURSES AND ACADEMICS (10) --------

("Academics", "What courses are offered by the college?",
 "The college offers various undergraduate and postgraduate courses. Check the official website for details.",
 "courses offered"),

("Academics", "Is Computer Science Engineering available?",
 "Please check the college course list or contact the academic department.",
 "computer science"),

("Academics", "How many semesters are there in engineering?",
 "Most four-year engineering programs have eight semesters.",
 "semesters engineering"),

("Academics", "When does the academic year start?",
 "The academic calendar is published by the college administration.",
 "academic year"),

("Academics", "Where can I get the syllabus?",
 "You can get the syllabus from your department or university website.",
 "syllabus"),

("Academics", "Are practical classes conducted?",
 "Yes, practical sessions are conducted according to the course timetable.",
 "practical classes"),

("Academics", "Can I get previous year question papers?",
 "Previous question papers may be available in the department or library.",
 "question papers"),

("Academics", "Who is the head of the department?",
 "Contact your department office for the current Head of Department details.",
 "hod department"),

("Academics", "Are extra classes conducted?",
 "Extra classes may be arranged by faculty members when required.",
 "extra classes"),

("Academics", "How can I contact my faculty?",
 "You can contact faculty members through the department or official college communication channels.",
 "contact faculty"),


# -------- FEES AND SCHOLARSHIPS (10) --------

("Fees", "What is the college fee structure?",
 "The fee structure depends on the course and admission category. Contact the accounts office.",
 "fee structure"),

("Fees", "How can I pay my college fees?",
 "Fees can be paid through the payment methods approved by the college.",
 "pay fees"),

("Fees", "Is online fee payment available?",
 "Check with the accounts department for available online payment facilities.",
 "online payment"),

("Fees", "Can I pay fees in installments?",
 "Installment facilities depend on college rules. Contact the accounts office.",
 "installment fees"),

("Fees", "Are scholarships available?",
 "Eligible students may apply for government and institutional scholarships.",
 "scholarships"),

("Fees", "How can I apply for a scholarship?",
 "You can apply through the relevant scholarship portal and submit the required documents.",
 "apply scholarship"),

("Fees", "Is there a fee concession?",
 "Fee concessions may be available for eligible students according to applicable rules.",
 "fee concession"),

("Fees", "Where is the accounts office?",
 "Visit the college administration building to locate the accounts office.",
 "accounts office"),

("Fees", "Can I get a fee receipt?",
 "Yes, you can request a fee receipt from the accounts department.",
 "fee receipt"),

("Fees", "What happens if I pay fees late?",
 "Late payment rules and applicable penalties are determined by the college.",
 "late fees"),


# -------- EXAMINATIONS (10) --------

("Examinations", "When are internal exams conducted?",
 "Internal examination dates are announced by the respective departments.",
 "internal exams"),

("Examinations", "When are semester exams conducted?",
 "Semester examination schedules are announced by the university.",
 "semester exams"),

("Examinations", "Where can I get the exam timetable?",
 "You can get the examination timetable from the university website or department notice board.",
 "exam timetable"),

("Examinations", "What is the passing percentage?",
 "Passing requirements depend on university examination regulations.",
 "passing percentage"),

("Examinations", "What is a backlog?",
 "A backlog is a subject that a student has not successfully cleared.",
 "backlog"),

("Examinations", "Can I apply for revaluation?",
 "Yes, eligible students can apply for revaluation according to university guidelines.",
 "revaluation"),

("Examinations", "How can I check my results?",
 "Results are generally published on the official university result portal.",
 "exam results"),

("Examinations", "What is an internal assessment?",
 "Internal assessment evaluates student performance through tests, assignments and other academic activities.",
 "internal assessment"),

("Examinations", "What should I carry to the examination hall?",
 "Carry your examination hall ticket and permitted stationery.",
 "exam hall"),

("Examinations", "What happens if I miss an examination?",
 "Contact your department immediately to understand the applicable university rules.",
 "miss exam"),


# -------- ATTENDANCE (10) --------

("Attendance", "What is the minimum attendance requirement?",
 "The minimum attendance requirement depends on university regulations.",
 "minimum attendance"),

("Attendance", "How can I check my attendance?",
 "You can check your attendance through the student portal or contact your faculty.",
 "check attendance"),

("Attendance", "Can I get attendance for medical reasons?",
 "Medical leave and attendance considerations are subject to university rules.",
 "medical attendance"),

("Attendance", "Who maintains attendance records?",
 "Subject faculty members generally maintain attendance records.",
 "attendance records"),

("Attendance", "What happens if my attendance is low?",
 "Low attendance may affect your examination eligibility according to university rules.",
 "low attendance"),

("Attendance", "Is attendance compulsory?",
 "Yes, students are expected to attend classes regularly.",
 "attendance compulsory"),

("Attendance", "Can I apply for leave?",
 "Yes, submit a leave application to the appropriate faculty or department.",
 "apply leave"),

("Attendance", "How do I correct attendance mistakes?",
 "Contact the respective subject faculty with the relevant details.",
 "attendance correction"),

("Attendance", "Is attendance calculated subject-wise?",
 "Attendance is generally maintained separately for each subject.",
 "subject attendance"),

("Attendance", "Where can I submit a medical certificate?",
 "Submit your medical certificate to your department or designated college office.",
 "medical certificate"),


# -------- LIBRARY (10) --------

("Library", "What are the library timings?",
 "Library timings are displayed at the library entrance or on the college notice board.",
 "library timings"),

("Library", "How can I get a library card?",
 "Register with the library and follow the membership procedure.",
 "library card"),

("Library", "How many books can I borrow?",
 "The number of books depends on the library borrowing policy.",
 "borrow books"),

("Library", "Can I renew borrowed books?",
 "Yes, book renewal is subject to library rules and availability.",
 "renew books"),

("Library", "What happens if I return books late?",
 "Late return may result in a fine according to library rules.",
 "late return"),

("Library", "Is Wi-Fi available in the library?",
 "Check with the library staff for available internet facilities.",
 "library wifi"),

("Library", "Can I access digital books?",
 "Digital learning resources may be available through the library.",
 "digital books"),

("Library", "Is there a reading room?",
 "Contact the library staff to know about reading room facilities.",
 "reading room"),

("Library", "Can I study in the library?",
 "Yes, students can use the library for individual study.",
 "study library"),

("Library", "Who should I contact for library issues?",
 "Contact the librarian or library staff.",
 "library help"),


# -------- HOSTEL (10) --------

("Hostel", "Does the college provide hostel facilities?",
 "Hostel availability depends on the facilities provided by the college.",
 "hostel facilities"),

("Hostel", "How can I apply for a hostel?",
 "Contact the hostel administration to complete the application process.",
 "hostel apply"),

("Hostel", "Are separate hostels available for boys and girls?",
 "Hostel accommodation arrangements depend on college facilities.",
 "boys girls hostel"),

("Hostel", "What are the hostel timings?",
 "Hostel entry and exit timings are communicated by hostel administration.",
 "hostel timings"),

("Hostel", "Is food provided in the hostel?",
 "Food availability and meal arrangements depend on hostel facilities.",
 "hostel food"),

("Hostel", "Is Wi-Fi available in the hostel?",
 "Contact hostel administration to confirm internet availability.",
 "hostel wifi"),

("Hostel", "Can visitors enter the hostel?",
 "Visitor entry is governed by hostel security and visitor policies.",
 "hostel visitors"),

("Hostel", "Whom should I contact for hostel complaints?",
 "Contact the hostel warden or hostel administration.",
 "hostel complaints"),

("Hostel", "Is laundry available in the hostel?",
 "Check with hostel administration for laundry facilities.",
 "hostel laundry"),

("Hostel", "Can I leave the hostel during weekends?",
 "Weekend outing permissions depend on hostel rules.",
 "hostel weekends"),


# -------- PLACEMENT AND INTERNSHIP (10) --------

("Placement", "Does the college provide placement opportunities?",
 "The placement department coordinates recruitment opportunities for eligible students.",
 "placements"),

("Placement", "Where is the placement cell?",
 "Contact the college administration to locate the placement cell.",
 "placement cell"),

("Placement", "Which companies visit the college?",
 "Company visits vary each year. Contact the placement department for the latest information.",
 "companies placements"),

("Placement", "Are internships provided?",
 "The placement department may share internship opportunities with students.",
 "internships"),

("Placement", "How can I register for placements?",
 "Register through the college placement cell according to its instructions.",
 "placement registration"),

("Placement", "Are aptitude classes conducted?",
 "The college may organize aptitude and placement training sessions.",
 "aptitude classes"),

("Placement", "Is resume preparation training available?",
 "Contact the placement department for resume-building workshops.",
 "resume training"),

("Placement", "Can first-year students apply for internships?",
 "Some internships accept first-year students. Check the eligibility requirements of each opportunity.",
 "first year internship"),

("Placement", "Are coding classes provided?",
 "Check with your department or placement cell for coding training programs.",
 "coding classes"),

("Placement", "How can I prepare for campus placements?",
 "Improve your technical knowledge, communication skills, aptitude and problem-solving abilities.",
 "placement preparation"),


# -------- CAMPUS FACILITIES (10) --------

("Facilities", "Is Wi-Fi available on campus?",
 "Contact the IT department to know about campus Wi-Fi access.",
 "campus wifi"),

("Facilities", "Is there a canteen?",
 "Check the college campus facilities for canteen availability.",
 "canteen"),

("Facilities", "Are sports facilities available?",
 "The college may provide sports facilities for various activities.",
 "sports facilities"),

("Facilities", "Is there a medical room?",
 "Contact the college administration for information about medical facilities.",
 "medical room"),

("Facilities", "Is parking available?",
 "Parking facilities and permissions depend on college regulations.",
 "parking"),

("Facilities", "Is there a computer lab?",
 "Computer laboratories are generally available for practical academic sessions.",
 "computer lab"),

("Facilities", "Is transportation provided?",
 "Contact the transport department for bus routes and availability.",
 "transport"),

("Facilities", "Is there an auditorium?",
 "Contact the administration to know about auditorium facilities.",
 "auditorium"),

("Facilities", "Are extracurricular activities conducted?",
 "Students can participate in cultural events, clubs and extracurricular activities.",
 "extracurricular"),

("Facilities", "Is there a student activity club?",
 "Contact your department or student coordinator to learn about available clubs.",
 "student clubs"),


# -------- GENERAL INFORMATION (10) --------

("General", "What are the college working hours?",
 "College working hours are available on the official college timetable.",
 "working hours"),

("General", "Where is the principal office?",
 "Contact the administration office for directions to the principal's office.",
 "principal office"),

("General", "How can I contact the college?",
 "Use the contact information published on the official college website.",
 "contact college"),

("General", "Is there a student grievance cell?",
 "Contact the college administration for information about the student grievance cell.",
 "grievance cell"),

("General", "How can I get a bonafide certificate?",
 "Apply through the college administration or student service office.",
 "bonafide certificate"),

("General", "How can I get a transfer certificate?",
 "Submit a request to the college administration according to its procedure.",
 "transfer certificate"),

("General", "Are cultural events conducted?",
 "Yes, colleges generally organize cultural programs and student activities.",
 "cultural events"),

("General", "Where can I find college announcements?",
 "Check the college notice board, student portal and official communication channels.",
 "announcements"),

("General", "How can I report a lost ID card?",
 "Contact the administration office to report the lost ID card and request a replacement.",
 "lost id card"),

("General", "Who should I contact for general enquiries?",
 "Contact the college reception or administration office.",
 "general enquiries")

]


# ==========================================
# STEP 2: CREATE CSV FILE
# ==========================================

filename = "faq_data.csv"

def create_csv():

    with open(filename, "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow([
            "Category",
            "Question",
            "Answer",
            "Keywords"
        ])

        writer.writerows(faq_data)

    print("CSV file created successfully!")

    print("Total FAQs:", len(faq_data))


# ==========================================
# STEP 3: READ CSV FILE
# ==========================================

def load_faq():

    faqs = []

    with open(filename, "r", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:

            faqs.append(row)

    return faqs


# ==========================================
# STEP 4: PROCESS USER QUESTION
# ==========================================

def clean_text(text):

    text = text.lower()

    text = re.sub(r'[^a-z0-9\s]', '', text)

    return text


# ==========================================
# STEP 5: FIND BEST MATCH
# ==========================================

def find_answer(user_question, faqs):

    user_question = clean_text(user_question)

    best_match = None

    highest_score = 0

    user_words = set(user_question.split())

    for faq in faqs:

        question = clean_text(faq["Question"])

        keywords = clean_text(faq["Keywords"])

        combined_text = question + " " + keywords

        faq_words = set(combined_text.split())

        # Calculate word similarity

        common_words = user_words.intersection(faq_words)

        if len(user_words.union(faq_words)) > 0:

            word_score = (
                len(common_words) /
                len(user_words.union(faq_words))
            )

        else:

            word_score = 0

        # Calculate text similarity

        similarity = SequenceMatcher(
            None,
            user_question,
            question
        ).ratio()

        # Final matching score

        score = (word_score * 0.6) + (similarity * 0.4)

        if score > highest_score:

            highest_score = score

            best_match = faq

    # Minimum matching threshold

    if highest_score >= 0.20:

        return best_match

    else:

        return None


# ==========================================
# STEP 6: CHATBOT
# ==========================================

def chatbot():

    print("\n===================================")

    print("     COLLEGE FAQ CHATBOT")

    print("===================================")

    print("Hello! Welcome to College FAQ Chatbot.")

    print("I can answer 100 college-related questions.")

    print("Type 'exit' to stop the chatbot.")

    print("-----------------------------------")

    faqs = load_faq()

    while True:

        user_question = input("\nYou: ")

        if user_question.lower() in ["exit", "quit", "bye"]:

            print("\nChatbot: Thank you for using our chatbot!")

            print("Have a great day!")

            break

        if user_question.strip() == "":

            print("Chatbot: Please enter a question.")

            continue

        # Find the appropriate answer

        result = find_answer(user_question, faqs)

        if result:

            print("\nChatbot:")

            print(result["Answer"])

            print("\nCategory:", result["Category"])

        else:

            print("\nChatbot: Sorry, I couldn't understand your question.")

            print("Please contact the college administration for assistance.")

            print("You can also try asking in a different way.")


# ==========================================
# STEP 7: MAIN PROGRAM
# ==========================================

if __name__ == "__main__":

    create_csv()

    chatbot()