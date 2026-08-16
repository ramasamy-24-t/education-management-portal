DEMO_EMAIL_DOMAIN = "edu.example.com"
DEFAULT_SCHOOL_SLUG = "kit-campus"
DEFAULT_SCHOOL_NAME = "KIT Campus"
SECOND_SCHOOL_SLUG = "riverside"
SECOND_SCHOOL_NAME = "Riverside Academy"

FALLBACK_STUDY_TIPS = [
    "Review yesterday's notes for 10 minutes before starting new material.",
    "After each lecture, write three questions you still cannot answer.",
    "Space practice across days — short sessions beat one long cram.",
    "Teach a concept out loud. If you stall, that is the weak topic to revisit.",
    "Use your attendance and grade history to pick the next subject to review.",
]


def questions_for_course(title: str = "", category: str = "") -> list[dict]:
    """Course-specific MCQ paper; falls back to the generic study-habit set."""
    blob = f"{title} {category}".lower()
    if "python" in blob:
        return PYTHON_EXAM_QUESTIONS
    if "linear" in blob or "algebra" in blob:
        return ALGEBRA_EXAM_QUESTIONS
    if "history" in blob:
        return HISTORY_EXAM_QUESTIONS
    if "data structure" in blob:
        return DATA_STRUCTURES_EXAM_QUESTIONS
    if "stat" in blob:
        return STATISTICS_EXAM_QUESTIONS
    return list(DEFAULT_EXAM_QUESTIONS)


DEFAULT_EXAM_QUESTIONS = [
    {
        "prompt": "Which study habit improves long-term recall the most?",
        "options": [
            "Cramming everything the night before",
            "Spaced practice over several days",
            "Rereading notes once",
            "Skipping review after a good score",
        ],
        "correct": 1,
    },
    {
        "prompt": "A student missed two recent classes. What should they do first?",
        "options": [
            "Ignore the absences if exams went well",
            "Copy a classmate's assignment answers",
            "Review the missed lecture notes and ask the teacher one clarifying question",
            "Drop the course immediately",
        ],
        "correct": 2,
    },
    {
        "prompt": "When an exam analysis lists weak topics, the best next step is to:",
        "options": [
            "Only restudy topics that already feel easy",
            "Practice those weak topics with short drills",
            "Wait until the final exam",
            "Ask a friend to take the next test",
        ],
        "correct": 1,
    },
    {
        "prompt": "Which attendance pattern is healthiest for learning?",
        "options": [
            "Present most days, with makeup work after any absence",
            "Absent every other session",
            "Late every day but never absent",
            "Present only in the week before exams",
        ],
        "correct": 0,
    },
]

PYTHON_EXAM_QUESTIONS = [
    {
        "prompt": "Which Python type is mutable?",
        "options": ["tuple", "str", "list", "int"],
        "correct": 2,
    },
    {
        "prompt": "What does `len({1, 1, 2})` return?",
        "options": ["3", "2", "1", "It raises TypeError"],
        "correct": 1,
    },
    {
        "prompt": "The best way to open a text file for reading is:",
        "options": [
            "open(path, 'w')",
            "with open(path, encoding='utf-8') as handle:",
            "file = path.read()",
            "eval(path)",
        ],
        "correct": 1,
    },
    {
        "prompt": "A function should return a value when you need to:",
        "options": [
            "Print a message only",
            "Reuse the result in later code",
            "Crash the program",
            "Skip the next line",
        ],
        "correct": 1,
    },
]

ALGEBRA_EXAM_QUESTIONS = [
    {
        "prompt": "A 2×3 matrix times a 3×1 vector yields a:",
        "options": ["3×2 matrix", "2×1 vector", "3×3 matrix", "scalar only"],
        "correct": 1,
    },
    {
        "prompt": "The determinant of a 2×2 matrix [[a, b], [c, d]] is:",
        "options": ["a + d", "ad − bc", "ab − cd", "ac + bd"],
        "correct": 1,
    },
    {
        "prompt": "Eigenvectors of A satisfy:",
        "options": ["Av = 0 only", "Av = λv for some scalar λ", "A = vλ", "v must be the zero vector"],
        "correct": 1,
    },
    {
        "prompt": "Two vectors are orthogonal when their dot product is:",
        "options": ["1", "−1", "0", "undefined"],
        "correct": 2,
    },
]

HISTORY_EXAM_QUESTIONS = [
    {
        "prompt": "World War I ended in:",
        "options": ["1914", "1918", "1939", "1945"],
        "correct": 1,
    },
    {
        "prompt": "The Cold War is best described as:",
        "options": [
            "A direct US–USSR land war in Europe",
            "A long rivalry short of full-scale war between blocs",
            "The alliance that defeated Napoleon",
            "A trade pact limited to East Asia",
        ],
        "correct": 1,
    },
    {
        "prompt": "Decolonization after 1945 mainly meant:",
        "options": [
            "European empires expanding in Africa",
            "Colonies gaining independence from imperial powers",
            "The end of all nation-states",
            "A return to medieval kingdoms",
        ],
        "correct": 1,
    },
    {
        "prompt": "Late-20th-century globalization is associated with:",
        "options": [
            "Closed national markets only",
            "Faster trade, capital, and information flows",
            "The invention of agriculture",
            "The fall of the Roman Empire",
        ],
        "correct": 1,
    },
]

DATA_STRUCTURES_EXAM_QUESTIONS = [
    {
        "prompt": "Which structure is LIFO?",
        "options": ["Queue", "Stack", "Hash set", "B-tree"],
        "correct": 1,
    },
    {
        "prompt": "Average-case lookup in a well-sized hash table is:",
        "options": ["O(n)", "O(log n)", "O(1)", "O(n log n)"],
        "correct": 2,
    },
    {
        "prompt": "A binary search tree’s in-order traversal visits keys:",
        "options": ["In random order", "In sorted order", "Level by level only", "From the leaves first"],
        "correct": 1,
    },
    {
        "prompt": "BFS on an unweighted graph finds:",
        "options": [
            "A longest path",
            "A shortest path in number of edges",
            "The minimum spanning tree",
            "All topological sorts",
        ],
        "correct": 1,
    },
]

STATISTICS_EXAM_QUESTIONS = [
    {
        "prompt": "The median is:",
        "options": [
            "The most frequent value",
            "The middle value of ordered data",
            "The sum of values divided by n",
            "Always equal to the mean",
        ],
        "correct": 1,
    },
    {
        "prompt": "A p-value is:",
        "options": [
            "The probability the null is true",
            "The chance of data at least this extreme if the null is true",
            "The sample size",
            "The confidence interval width",
        ],
        "correct": 1,
    },
    {
        "prompt": "A larger random sample usually:",
        "options": [
            "Increases sampling error",
            "Reduces sampling error",
            "Removes all bias",
            "Makes the mean undefined",
        ],
        "correct": 1,
    },
    {
        "prompt": "A histogram is most useful for:",
        "options": [
            "Showing the shape of a numeric distribution",
            "Listing every raw row",
            "Replacing a hypothesis test",
            "Computing a p-value directly",
        ],
        "correct": 0,
    },
]
