import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UnstructuredComponent } from './unstructured.component';

describe('UnstructuredComponent', () => {
  let component: UnstructuredComponent;
  let fixture: ComponentFixture<UnstructuredComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UnstructuredComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UnstructuredComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
