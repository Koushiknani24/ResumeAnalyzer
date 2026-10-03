import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_tfidf_similarity(resume_text: str, job_description: str) -> float:
    """
    Calculates the classic TF-IDF Cosine Similarity score.
    """
    try:
        if not resume_text.strip() or not job_description.strip():
            return 0.0
            
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform([resume_text, job_description])
        similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        score = similarity_matrix[0][0] * 100
        return round(score, 2)
    except Exception as e:
        print(f"Error calculating TF-IDF: {e}")
        return 0.0

def generate_competition_plot(match_score: float):
    """
    Generates a classic Matplotlib figure showing a normal distribution curve.
    """
    np.random.seed(42)
    simulated_scores = np.random.normal(loc=60, scale=15, size=1000)
    simulated_scores = np.clip(simulated_scores, 0, 100)
    
    df = pd.DataFrame(simulated_scores, columns=['Score'])
    
    fig, ax = plt.subplots(figsize=(8, 4))
    
    ax.hist(df['Score'], bins=30, density=True, alpha=0.5, color='#4A90E2', label="Other Applicants")
    
    xmin, xmax = ax.get_xlim()
    x = np.linspace(xmin, xmax, 100)
    p = (1 / (15 * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - 60) / 15) ** 2)
    ax.plot(x, p, 'k', linewidth=2, color='#1A1A1A')
    
    ax.axvline(match_score, color='red', linestyle='dashed', linewidth=2.5, label=f"Your Score ({match_score})")
    
    ax.set_title("Applicant Score Distribution", fontsize=14, fontweight='bold')
    ax.set_xlabel("Match Score (0-100)", fontsize=12)
    ax.set_ylabel("Density", fontsize=12)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.legend(loc="upper right")
    fig.tight_layout()
    
    return fig
