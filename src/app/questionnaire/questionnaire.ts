import { Component } from '@angular/core';
import { Api } from '../api.service';

interface Question {
  id: number;
  text: string;
  type: 'choice' | 'slider' | 'yesno';
  options?: string[];
  min?: number;
  max?: number;
  section: string;
  answer?: any;
}

@Component({
  selector: 'app-questionnaire',
  standalone: false,
  templateUrl: './questionnaire.html',
  styleUrl: './questionnaire.css'
})
export class Questionnaire {
  predictionResult: number | null = null;
  constructor(private api: Api) {}

    questions: Question[] = [
  { id: 1, text: 'What is your age?', type: 'slider', section: 'Demographics', min: 12, max: 35 },
  { id: 2, text: 'What is your gender?', type: 'choice', section: 'Demographics', options: ['Female', 'Male', 'Prefer not to say'] },
  { id: 3, text: 'What is your grade level?', type: 'choice', section: 'Demographics', options: ['1st Year', '2nd Year', '3rd Year', '4th Year', '5th Year', 'Grade 10', 'Grade 11', 'Grade 12'] },
  { id: 4, text: 'What is your strand/track?', type: 'choice', section: 'Demographics', options: ['ABM', 'BMMA', 'BSA', 'BSA-ANSCI', 'BSAMT', 'BSARC', 'BSBIO', 'BSBIO-EBIO', 'BSCE', 'BSCJ', 'BSCPE', 'BSCS', 'BSED', 'BSESS', 'BSIT', 'BSMLS', 'BSMarE', 'BSN', 'BSPSYCH', 'BSPT', 'BSTM', 'HUMSS', 'ICT', 'JHS', 'STEM'] },
  { id: 5, text: 'What is your main internet access?', type: 'choice', section: 'Digital Behavior', options: ['Home Wi-Fi (Personal/Family Router)', 'Mobile Data', 'Wired/Broadband (LAN/Ethernet)', 'Shared Wi-Fi (Dormitory, Boarding House, Hotspot)'] },
  { id: 6, text: 'What device(s) do you use?', type: 'choice', section: 'Digital Behavior', options: ['Desktop PC', 'Smartphone', 'Laptop', 'Tablet'] },
  { id: 7, text: 'How many hours per day do you spend on digital devices?', type: 'slider', section: 'Digital Behavior', min: 0, max: 16 },
  { id: 8, text: 'Do you use digital devices within 1 hour before sleeping?', type: 'yesno', section: 'Digital Behavior' }
];
  page = 0;
  pageSize = 1;

  get currentQuestion(): Question {
    return this.questions[this.page];
  }
  resetQuestions() {
  this.page = 0;
  this.predictionResult = null;
  this.questions.forEach(q => q.answer = undefined);
}

  next(){
    if (this.currentQuestion.answer) this.page++;
    else alert('Please answer before proceeding.');
  }

  prev(){
    if (this.page > 0) this.page--;
  }

  submit() {
    if (this.questions.every(q => q.answer)) {
      const responses = this.questions.map(q => ({
        question_id: q.id,
        answer: q.answer
      }));
      this.api.submitResponses(responses).subscribe({
        next: (result) => {
          this.predictionResult = result.prediction || 'No prediction received.';
        },
        error: () => alert('Submission failed!')
      });
    } else {
      alert('Please answer all questions.');
    }
  }
}
