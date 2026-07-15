const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://ai-resume-analyzer-haf2.onrender.com/api'; 

export async function checkApiHealth() {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    if (!response.ok) {
      throw new Error('API health check failed');
    }
    return await response.json();
  } catch (error) {
    console.error('API health check error:', error);
    return { status: 'offline', error: error.message };
  }
}

export async function analyzeResume(file, jobDescription) {
  const formData = new FormData();
  formData.append('file', file);
  if (jobDescription) {
    formData.append('job_description', jobDescription);
  }

  const response = await fetch(`${API_BASE_URL}/analyze`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `Server error (${response.status})`);
  }

  return await response.json();
}

export async function optimizeBulletPoint(bulletPoint) {
  const response = await fetch(`${API_BASE_URL}/optimize-bullet`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ bullet_point: bulletPoint }),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `Server error (${response.status})`);
  }

  return await response.json();
}
