import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SemiStructuredComponent } from './semi-structured.component';

describe('SemiStructuredComponent', () => {
  let component: SemiStructuredComponent;
  let fixture: ComponentFixture<SemiStructuredComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SemiStructuredComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SemiStructuredComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
