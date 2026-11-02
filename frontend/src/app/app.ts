import { 
    Component,
    signal,
    AfterViewInit,
    OnDestroy,
    ViewChild,
    ElementRef,
    inject
} from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { Subscription, timer, concatMap } from 'rxjs';

interface Point {
    x: number;
    y: number;
}

interface WorldState {
    width: number;
    height: number;
    prey: Point[];
    food: Point[];
}

@Component({
    imports: [RouterOutlet],
    selector: 'app-root',
    styleUrl: './app.css',
    templateUrl: './app.html',
})
export class App implements AfterViewInit, OnDestroy {
    protected readonly title = signal('frontend');
    @ViewChild('worldCanvas')
    canvas!: ElementRef<HTMLCanvasElement>;

    private http = inject(HttpClient);
    private updates?: Subscription;

    ngAfterViewInit() {
        this.updates = timer(0, 100)
            .pipe(
                concatMap(() =>
                    this.http.post<WorldState>(
                        'http://127.0.0.1:8000/simulation/step',
                        {}
                    )
                )
            )
            .subscribe(state => this.draw(state));
    }

    private draw(state: WorldState) {
        const canvas = this.canvas.nativeElement;
        const ctx = canvas.getContext('2d')!;

        ctx.clearRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = 'green';

        for (const food of state.food) {
            ctx.beginPath();
            ctx.arc(food.x, food.y, 4, 0, Math.PI * 2);
            ctx.fill();
        }

        ctx.fillStyle = 'red';

        for (const prey of state.prey) {
            ctx.beginPath();
            ctx.arc(prey.x, prey.y, 8, 0, Math.PI * 2);
            ctx.fill();
        }
    }

    ngOnDestroy() {
        this.updates?.unsubscribe();
    }
}