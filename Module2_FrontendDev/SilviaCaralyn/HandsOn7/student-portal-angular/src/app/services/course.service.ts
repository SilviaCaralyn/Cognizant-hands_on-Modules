import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map } from 'rxjs';

export interface Course {
  id: number;
  name: string;
  code: string;
  credits: number;
  grade: string;
}

const FALLBACK_META = [
  { credits: 4, grade: 'A' },
  { credits: 4, grade: 'B+' },
  { credits: 3, grade: 'A-' },
  { credits: 4, grade: 'A' },
  { credits: 3, grade: 'B' },
];

@Injectable({ providedIn: 'root' }) // singleton, shared across the whole app
export class CourseService {
  constructor(private http: HttpClient) {}

  getCourses(): Observable<Course[]> {
    return this.http
      .get<any[]>('https://jsonplaceholder.typicode.com/posts?_limit=5')
      .pipe(
        map((posts) =>
          posts.map((post, index) => ({
            id: post.id,
            name: post.title.slice(0, 24),
            code: `CS${100 + index}`,
            credits: FALLBACK_META[index % FALLBACK_META.length].credits,
            grade: FALLBACK_META[index % FALLBACK_META.length].grade,
          }))
        )
      );
  }
}
