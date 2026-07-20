import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-course-card',
  standalone: true,
  imports: [],
  templateUrl: './course-card.component.html',
})
export class CourseCardComponent {
  @Input() name = '';
  @Input() code = '';
  @Input() credits = 0;
  @Input() grade = '';
}
