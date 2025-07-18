import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class Api {
  private apiUrl = 'http://localhost:8000/api/responses/'; // Update if your Django API runs elsewhere

  constructor(private http: HttpClient) {}

  submitResponses(responses: any[]): Observable<any> {
    // Assumes your Django API expects a list of responses
    return this.http.post(this.apiUrl, responses);
  }
}
