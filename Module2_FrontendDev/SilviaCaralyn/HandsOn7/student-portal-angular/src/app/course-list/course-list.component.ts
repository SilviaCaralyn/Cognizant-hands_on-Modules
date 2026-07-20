import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CourseCardComponent } from '../course-card/course-card.component';
import { CourseService, Course } from '../services/course.service';

@Component({
  selector: 'app-course-list',
  standalone: true,
  imports: [CommonModule, FormsModule, CourseCardComponent],
  templateUrl: './course-list.component.html',
})
export class CourseListComponent implements OnInit {
  courses: Course[] = [];
  searchTerm = '';
  loading = true;
  error: string | null = null;

  constructor(private courseService: CourseService) {}

  ngOnInit(): void {
    this.loading = true;
    this.courseService.getCourses().subscribe({
      next: (data) => {
        this.courses = data;
        this.loading = false;
      },
      error: (err) => {
        this.error = err.message ?? 'Failed to load courses';
        this.loading = false;
      },
    });
  }

  get filteredCourses(): Course[] {
    const term = this.searchTerm.toLowerCase();
    return this.courses.filter((c) => c.name.toLowerCase().includes(term));
  }
}
