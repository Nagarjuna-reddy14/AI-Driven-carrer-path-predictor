/**
 * Complete Dashboard and Analysis Components
 * Includes resume upload, skill input, career predictions, and roadmap display
 */

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { analysisAPI, predictionAPI, roadmapAPI } from '../services/api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ResponsiveContainer } from 'recharts';

// Complete Analysis Component
export function CompleteDashboard() {
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  // Form data
  const [resumeFile, setResumeFile] = useState(null);
  const [education, setEducation] = useState('');
  const [manualSkills, setManualSkills] = useState('');
  const [interests, setInterests] = useState('');
  const [experienceYears, setExperienceYears] = useState(0);
  
  // Results
  const [extractedSkills, setExtractedSkills] = useState([]);
  const [predictions, setPredictions] = useState(null);
  const [roadmap, setRoadmap] = useState(null);

  const navigate = useNavigate();

  const handleResumeUpload = async () => {
    if (!resumeFile) {
      setError('Please select a PDF file');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await analysisAPI.analyzeResume(resumeFile);
      setExtractedSkills(response.data.skills || []);
      setStep(2);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to analyze resume');
    } finally {
      setLoading(false);
    }
  };

  const handleSkipResume = () => {
    setStep(2);
  };

  const handleGeneratePredictions = async () => {
    const allSkills = [...new Set([...extractedSkills, ...manualSkills.split(',').map(s => s.trim()).filter(Boolean)])];
    const interestsList = interests.split(',').map(s => s.trim()).filter(Boolean);

    if (allSkills.length === 0) {
      setError('Please add at least one skill');
      return;
    }

    setLoading(true);
    setError('');

    try {
      // Predict careers
      const predResponse = await predictionAPI.predictCareers({
        education,
        skills: allSkills,
        interests: interestsList,
        experience_years: parseInt(experienceYears)
      });

      setPredictions(predResponse.data);
      setStep(3);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate predictions');
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateRoadmap = async (careerPath, missingSkills) => {
    setLoading(true);
    setError('');

    try {
      const allSkills = [...new Set([...extractedSkills, ...manualSkills.split(',').map(s => s.trim()).filter(Boolean)])];
      
      const roadmapResponse = await roadmapAPI.generateRoadmap(
        careerPath,
        missingSkills,
        allSkills
      );

      setRoadmap(roadmapResponse.data);
      setStep(4);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate roadmap');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <nav className="bg-white shadow-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <span className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              CareerPath AI
            </span>
            <button
              onClick={() => navigate('/dashboard')}
              className="px-4 py-2 text-gray-700 hover:text-gray-900"
            >
              ← Back to Dashboard
            </button>
          </div>
        </div>
      </nav>

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Progress Steps */}
        <div className="mb-12">
          <div className="flex justify-between items-center">
            {[
              { num: 1, label: 'Upload Resume' },
              { num: 2, label: 'Add Details' },
              { num: 3, label: 'View Predictions' },
              { num: 4, label: 'Get Roadmap' }
            ].map((s, idx) => (
              <div key={idx} className="flex items-center flex-1">
                <div className="flex flex-col items-center flex-1">
                  <div className={`w-12 h-12 rounded-full flex items-center justify-center font-bold text-lg ${
                    step >= s.num ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-600'
                  }`}>
                    {s.num}
                  </div>
                  <span className="mt-2 text-sm font-medium text-gray-700">{s.label}</span>
                </div>
                {idx < 3 && (
                  <div className={`h-1 flex-1 mx-2 ${step > s.num ? 'bg-blue-600' : 'bg-gray-200'}`} />
                )}
              </div>
            ))}
          </div>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-6 py-4 rounded-xl mb-6">
            {error}
          </div>
        )}

        {/* Step 1: Resume Upload */}
        {step === 1 && (
          <div className="bg-white p-8 rounded-2xl shadow-xl">
            <h2 className="text-3xl font-bold mb-6">Upload Your Resume</h2>
            <p className="text-gray-600 mb-8">We'll extract your skills using AI-powered NLP</p>

            <div className="border-2 border-dashed border-gray-300 rounded-xl p-12 text-center hover:border-blue-500 transition">
              <div className="text-6xl mb-4">📄</div>
              <input
                type="file"
                accept=".pdf"
                onChange={(e) => setResumeFile(e.target.files[0])}
                className="hidden"
                id="resume-upload"
              />
              <label htmlFor="resume-upload" className="cursor-pointer">
                <span className="text-blue-600 font-semibold hover:underline">
                  Choose PDF file
                </span>
                <span className="text-gray-600"> or drag and drop</span>
              </label>
              {resumeFile && (
                <p className="mt-4 text-gray-700 font-medium">{resumeFile.name}</p>
              )}
            </div>

            <div className="flex gap-4 mt-8">
              <button
                onClick={handleResumeUpload}
                disabled={!resumeFile || loading}
                className="flex-1 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition disabled:opacity-50"
              >
                {loading ? 'Analyzing...' : 'Analyze Resume'}
              </button>
              <button
                onClick={handleSkipResume}
                className="px-6 py-3 border border-gray-300 rounded-lg font-semibold hover:bg-gray-50 transition"
              >
                Skip
              </button>
            </div>
          </div>
        )}

        {/* Step 2: Add Details */}
        {step === 2 && (
          <div className="bg-white p-8 rounded-2xl shadow-xl">
            <h2 className="text-3xl font-bold mb-6">Complete Your Profile</h2>

            {extractedSkills.length > 0 && (
              <div className="mb-6 p-4 bg-green-50 rounded-lg">
                <h3 className="font-semibold text-green-800 mb-2">✓ Extracted Skills ({extractedSkills.length})</h3>
                <div className="flex flex-wrap gap-2">
                  {extractedSkills.slice(0, 10).map((skill, idx) => (
                    <span key={idx} className="px-3 py-1 bg-white rounded-full text-sm text-green-700 border border-green-200">
                      {skill}
                    </span>
                  ))}
                  {extractedSkills.length > 10 && (
                    <span className="px-3 py-1 text-sm text-green-600">+{extractedSkills.length - 10} more</span>
                  )}
                </div>
              </div>
            )}

            <div className="space-y-6">
              <div>
                <label className="block text-gray-700 font-medium mb-2">Education</label>
                <input
                  type="text"
                  value={education}
                  onChange={(e) => setEducation(e.target.value)}
                  placeholder="e.g., B.S. Computer Science"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>

              <div>
                <label className="block text-gray-700 font-medium mb-2">Additional Skills (comma-separated)</label>
                <textarea
                  value={manualSkills}
                  onChange={(e) => setManualSkills(e.target.value)}
                  placeholder="e.g., Python, React, Machine Learning, SQL"
                  rows="3"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-gray-700 font-medium mb-2">Interests (comma-separated)</label>
                <textarea
                  value={interests}
                  onChange={(e) => setInterests(e.target.value)}
                  placeholder="e.g., Artificial Intelligence, Web Development, Data Science"
                  rows="2"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-gray-700 font-medium mb-2">Years of Experience</label>
                <input
                  type="number"
                  value={experienceYears}
                  onChange={(e) => setExperienceYears(e.target.value)}
                  min="0"
                  max="50"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>

            <button
              onClick={handleGeneratePredictions}
              disabled={loading}
              className="w-full mt-8 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition disabled:opacity-50"
            >
              {loading ? 'Generating Predictions...' : 'Get Career Predictions →'}
            </button>
          </div>
        )}

        {/* Step 3: View Predictions */}
        {step === 3 && predictions && (
          <div className="space-y-6">
            <div className="bg-white p-8 rounded-2xl shadow-xl">
              <h2 className="text-3xl font-bold mb-6">Your Top Career Predictions</h2>

              {predictions.predictions && predictions.predictions.map((pred, idx) => (
                <div key={idx} className="mb-6 p-6 border-2 border-gray-200 rounded-xl hover:border-blue-500 transition">
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <h3 className="text-2xl font-bold text-gray-900">{pred.career_title}</h3>
                      <p className="text-gray-600 mt-2">{pred.description}</p>
                    </div>
                    <div className="text-right">
                      <div className="text-3xl font-bold text-blue-600">{Math.round(pred.confidence * 100)}%</div>
                      <div className="text-sm text-gray-500">Match</div>
                    </div>
                  </div>

                  <div className="grid md:grid-cols-2 gap-4 mb-4">
                    <div className="p-4 bg-green-50 rounded-lg">
                      <div className="text-sm text-gray-600 mb-1">Salary Range</div>
                      <div className="font-bold text-green-700">{pred.average_salary}</div>
                    </div>
                    <div className="p-4 bg-purple-50 rounded-lg">
                      <div className="text-sm text-gray-600 mb-1">Growth Rate</div>
                      <div className="font-bold text-purple-700">{pred.growth_rate}</div>
                    </div>
                  </div>

                  {idx === 0 && (
                    <button
                      onClick={() => handleGenerateRoadmap(pred.career_title, pred.missing_skills)}
                      className="w-full mt-4 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg font-semibold hover:shadow-lg transition"
                    >
                      Generate Learning Roadmap →
                    </button>
                  )}
                </div>
              ))}
            </div>

            {predictions.skill_gaps && (
              <div className="bg-white p-8 rounded-2xl shadow-xl">
                <h3 className="text-2xl font-bold mb-4">Skill Gap Analysis</h3>
                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <h4 className="font-semibold text-green-700 mb-2">✓ Matched Skills ({predictions.skill_gaps.matched_skills?.length || 0})</h4>
                    <div className="flex flex-wrap gap-2">
                      {predictions.skill_gaps.matched_skills?.slice(0, 10).map((skill, idx) => (
                        <span key={idx} className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm">
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>
                  <div>
                    <h4 className="font-semibold text-orange-700 mb-2">→ Skills to Learn ({predictions.skill_gaps.missing_skills?.length || 0})</h4>
                    <div className="flex flex-wrap gap-2">
                      {predictions.skill_gaps.missing_skills?.slice(0, 10).map((skill, idx) => (
                        <span key={idx} className="px-3 py-1 bg-orange-100 text-orange-700 rounded-full text-sm">
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Step 4: Roadmap */}
        {step === 4 && roadmap && (
          <div className="space-y-6">
            <div className="bg-white p-8 rounded-2xl shadow-xl">
              <h2 className="text-3xl font-bold mb-2">{roadmap.career_path} Learning Roadmap</h2>
              <p className="text-xl text-gray-600 mb-6">Estimated Timeline: {roadmap.timeline}</p>

              {roadmap.phases && roadmap.phases.map((phase, idx) => (
                <div key={idx} className="mb-6 p-6 bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl">
                  <h3 className="text-xl font-bold mb-2">Phase {phase.phase}: {phase.title}</h3>
                  <p className="text-gray-600 mb-3">{phase.focus} • {phase.duration}</p>
                  <div className="flex flex-wrap gap-2">
                    {phase.skills.map((skill, sidx) => (
                      <span key={sidx} className="px-3 py-1 bg-white rounded-full text-sm font-medium">
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>
              ))}
            </div>

            {roadmap.projects && roadmap.projects.length > 0 && (
              <div className="bg-white p-8 rounded-2xl shadow-xl">
                <h3 className="text-2xl font-bold mb-6">Recommended Projects</h3>
                <div className="grid md:grid-cols-2 gap-6">
                  {roadmap.projects.map((project, idx) => (
                    <div key={idx} className="p-6 border-2 border-gray-200 rounded-xl hover:border-blue-500 transition">
                      <h4 className="text-xl font-bold mb-2">{project.title}</h4>
                      <p className="text-gray-600 mb-3">{project.description}</p>
                      <div className="flex justify-between items-center text-sm">
                        <span className="text-blue-600 font-medium">{project.difficulty}</span>
                        <span className="text-gray-500">{project.estimated_time}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {roadmap.certifications && roadmap.certifications.length > 0 && (
              <div className="bg-white p-8 rounded-2xl shadow-xl">
                <h3 className="text-2xl font-bold mb-6">Recommended Certifications</h3>
                <div className="space-y-4">
                  {roadmap.certifications.map((cert, idx) => (
                    <div key={idx} className="p-4 bg-gray-50 rounded-lg">
                      <h4 className="font-bold">{cert.name}</h4>
                      <p className="text-gray-600">{cert.provider} • {cert.duration}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            <button
              onClick={() => navigate('/dashboard')}
              className="w-full py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition"
            >
              Back to Dashboard
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default CompleteDashboard;
