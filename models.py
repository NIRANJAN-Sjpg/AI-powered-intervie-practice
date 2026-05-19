from django.core.management.base import BaseCommand
from interviews.models import Question


QUESTIONS = [
    # ── Software Engineer ──────────────────────────────────────────────────
    {
        "text": "Tell me about yourself and why you want to become a software engineer.",
        "role": "software", "difficulty": "easy",
        "ideal_answer": "Briefly introduce your background, education, key projects (like your Django/React work), and passion for problem-solving. Mention relevant skills like Python, Django, REST APIs, and your final year project. End with why you're excited about this role."
    },
    {
        "text": "What is the difference between a list and a tuple in Python?",
        "role": "software", "difficulty": "easy",
        "ideal_answer": "A list is mutable (can be changed after creation) while a tuple is immutable (cannot be changed). Lists use square brackets [], tuples use parentheses (). Tuples are faster and used for fixed data. Example: list = [1,2,3], tuple = (1,2,3)."
    },
    {
        "text": "Explain what REST API is and how you have used it in your projects.",
        "role": "software", "difficulty": "medium",
        "ideal_answer": "REST API is an architectural style for building web services using HTTP methods (GET, POST, PUT, DELETE). It is stateless and uses JSON for data exchange. In my E-Blood Banking project, I built REST APIs using Django REST Framework to handle donor registration, blood requests, and availability checks."
    },
    {
        "text": "What is the difference between GET and POST HTTP methods?",
        "role": "software", "difficulty": "easy",
        "ideal_answer": "GET is used to retrieve data from the server. Data is sent in the URL and is visible. POST is used to send data to the server to create or update resources. Data is sent in the request body and is not visible in the URL. GET is cacheable; POST is not."
    },
    {
        "text": "Explain Object-Oriented Programming concepts with an example.",
        "role": "software", "difficulty": "medium",
        "ideal_answer": "OOP has four pillars: Encapsulation (bundling data and methods), Inheritance (child class inherits from parent), Polymorphism (same method behaves differently), and Abstraction (hiding complex details). Example: A 'Vehicle' class with 'Car' and 'Bike' as subclasses."
    },
    {
        "text": "What is the difference between SQL and NoSQL databases?",
        "role": "software", "difficulty": "medium",
        "ideal_answer": "SQL databases are relational, use structured tables, and support ACID transactions (e.g. MySQL, PostgreSQL). NoSQL databases are non-relational, store unstructured data in documents, key-value, or graph formats (e.g. MongoDB, Redis). SQL is better for complex queries; NoSQL scales better for large unstructured data."
    },
    {
        "text": "How would you handle a situation where your code is working locally but failing in production?",
        "role": "software", "difficulty": "hard",
        "ideal_answer": "First check error logs for specific error messages. Compare environment variables and dependencies between local and production. Look for missing packages in requirements.txt, database migration issues, or environment-specific config differences. Reproduce the issue step by step and apply a fix with proper testing."
    },
    {
        "text": "What is version control and how have you used Git?",
        "role": "software", "difficulty": "easy",
        "ideal_answer": "Version control tracks changes to code over time. Git is the most popular version control system. I have used Git for my projects by initializing repositories, making commits for each feature, creating branches for new features, and pushing code to GitHub for backup and collaboration."
    },

    # ── BPO / Customer Support ────────────────────────────────────────────
    {
        "text": "How would you handle an angry customer who is frustrated with a delayed order?",
        "role": "bpo", "difficulty": "easy",
        "ideal_answer": "First, listen patiently without interrupting. Empathize with the customer by saying 'I understand your frustration.' Apologize sincerely. Then check the order status, provide a clear update, and offer a resolution such as a refund, replacement, or expedited shipping. Thank them for their patience."
    },
    {
        "text": "Tell me about a time you dealt with a difficult situation and how you resolved it.",
        "role": "bpo", "difficulty": "medium",
        "ideal_answer": "Use the STAR method: Situation, Task, Action, Result. Describe a real example such as managing a group project conflict or handling a tough customer. Focus on your communication skills, calm approach, and how the situation was resolved successfully."
    },
    {
        "text": "Why do you want to work in a BPO? What motivates you?",
        "role": "bpo", "difficulty": "easy",
        "ideal_answer": "I enjoy interacting with people and solving their problems. BPO roles offer the opportunity to develop strong communication, problem-solving, and multitasking skills. I am motivated by customer satisfaction and the fast-paced environment. I also see it as a great starting point to grow in a company."
    },
    {
        "text": "How do you manage your time when handling multiple customer queries at once?",
        "role": "bpo", "difficulty": "medium",
        "ideal_answer": "I prioritize queries based on urgency. I use tools like ticketing systems to track open issues. I handle one customer at a time with full attention while using hold time productively to check information. I also communicate realistic timelines to customers so they feel informed."
    },

    # ── Data Analyst ──────────────────────────────────────────────────────
    {
        "text": "What is the difference between mean, median, and mode?",
        "role": "data", "difficulty": "easy",
        "ideal_answer": "Mean is the average of all values. Median is the middle value when sorted. Mode is the value that appears most frequently. Example: For [2, 3, 3, 5, 7] — Mean = 4, Median = 3, Mode = 3. Median is better than mean when there are extreme outliers."
    },
    {
        "text": "What Python libraries have you used for data analysis?",
        "role": "data", "difficulty": "easy",
        "ideal_answer": "I have used Pandas for data manipulation and cleaning, NumPy for numerical computation, Matplotlib and Seaborn for data visualization, and Scikit-learn for machine learning. In my movie recommendation project, I used Pandas and Scikit-learn to build a content-based filtering model."
    },
    {
        "text": "What is the difference between supervised and unsupervised learning?",
        "role": "data", "difficulty": "medium",
        "ideal_answer": "Supervised learning trains a model on labeled data where the output is known (e.g. classification, regression). Unsupervised learning finds patterns in unlabeled data without predefined outputs (e.g. clustering, dimensionality reduction). Examples: supervised — spam detection; unsupervised — customer segmentation."
    },

    # ── HR Round ──────────────────────────────────────────────────────────
    {
        "text": "Tell me about yourself.",
        "role": "hr", "difficulty": "easy",
        "ideal_answer": "Start with your name and degree. Mention your college and CGPA. Talk about your key projects briefly (2 sentences max). Mention your technical skills. End with why you're excited about this specific role and company. Keep it under 2 minutes."
    },
    {
        "text": "What are your strengths and weaknesses?",
        "role": "hr", "difficulty": "easy",
        "ideal_answer": "For strengths: mention 2-3 relevant ones with examples, e.g. problem-solving, quick learner, team player. For weakness: pick one genuine weakness but explain what you are doing to improve it. Example: 'I sometimes spend too much time perfecting code, but I have learned to prioritize based on deadlines.'"
    },
    {
        "text": "Where do you see yourself in 5 years?",
        "role": "hr", "difficulty": "easy",
        "ideal_answer": "In 5 years, I see myself as a skilled software engineer with deep expertise in full-stack development and AI. I want to contribute meaningfully to challenging projects, take on team responsibilities, and grow into a senior developer role within your organization."
    },
    {
        "text": "Why should we hire you over other candidates?",
        "role": "hr", "difficulty": "medium",
        "ideal_answer": "I bring a combination of technical skills (Python, Django, REST APIs, React), real project experience (E-Blood Banking, movie recommendation system), and a strong learning mindset. I have also completed an IBM certification and a UI/UX internship. I am a fresher who is dedicated, adaptable, and ready to contribute from day one."
    },
    {
        "text": "Are you comfortable working in shifts or relocating?",
        "role": "hr", "difficulty": "easy",
        "ideal_answer": "Yes, I am flexible and open to working in different shifts as required by the organization. I understand that IT and BPO roles may have rotational shifts and I am prepared for that. I am also open to relocation if the opportunity offers growth and a good work environment."
    },
]


class Command(BaseCommand):
    help = 'Seed the database with sample interview questions'

    def handle(self, *args, **kwargs):
        count = 0
        for q in QUESTIONS:
            _, created = Question.objects.get_or_create(
                text=q['text'],
                defaults={
                    'role': q['role'],
                    'difficulty': q['difficulty'],
                    'ideal_answer': q['ideal_answer'],
                }
            )
            if created:
                count += 1

        self.stdout.write(self.style.SUCCESS(f'✅ Seeded {count} new questions ({len(QUESTIONS)} total in DB)'))
