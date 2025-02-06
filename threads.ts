// создание класса семифор для управления потоками
class Semaphore{
    private count: number;
    private waiting: Array<() => void> = [];

    constructor(count: number) {
        this.count = count;
    }

    // Метод для получения доступа к ресурсу
    async acquire(): Promise<void> {
        if (this.count > 0) {
            this.count--;
            return Promise.resolve();
        }

        // Если все семафоры заняты, создаем новый промис и добавляем его в очередь ожидания
        return new Promise(resolve => {
            this.waiting.push(() => {
                this.count--;
                resolve();
            });
        });
    }

    // Метод для освобождения ресурса
    release(): void {
        this.count++;

        // Если есть ожидающие, вызываем один из них
        if (this.waiting.length > 0) {
            const next = this.waiting.shift();
            if (next) {
                next(); // Разрешаем следующий промис
            }
        }
    }
}

// имитация выполнения задачи через временной ресурс
function sleep(ms:number):Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// контракт задачи, интерфейс
interface ITask {
    id:number;
    status: 'running' | 'pending';
}

// исполнитель задач 
class Executor {
    private running:Map<number, ITask> = new Map();

    async executeTask(task:ITask) {
        if (this.running.has(task.id)) {
            console.log('stopped');
            throw new Error(`Task with id ${task.id} is running`);
        }
        this.running.set(task.id, task);
        console.log(`Task ${task.id} is running...`);
        await sleep(25);
        console.log(`Task ${task.id} is OK.`);
        this.running.delete(task.id);
    }
}

// создание исполнителя задачи 
const executor = new Executor();

// генерация задач для тестирования
// параллельного исполнения задачи
function* generateTasks(count:number, id:number=0):Generator<ITask> {
    for (let i:number=0; i <=count; i++) {
        yield {
            id:i,
            status:"running"
        }
    }
}

// тестирование общего случая 
// параллельного исполнения задач

async function testExecutor() {
    const testTasks = Array.from(generateTasks(5)); // Преобразуем генератор в массив
    // Запускаем все задачи параллельно и ждем завершения всех
    await Promise.all(testTasks.map(task => executor.executeTask(task)));
}

// ручное создание задач в виде AsyncIterable 
const task0:ITask = {id:0, status:"running"};
const task2:ITask = {id:1, status:"running"};
const task3:ITask = {id:2, status:"running"};
const task4:ITask = {id:3, status:"running"};
const task5:ITask = {id:4, status:"running"};
const task6:ITask = {id:5, status:"running"};
const task7:ITask = {id:5, status:"pending"};

const Iterable:ITask[] = [
    task0, task0, task2,task3,task4, task5, task6, task7
];

async function manTestExecutor(iterable:ITask[]) {
    await Promise.all(iterable.map(task => executor.executeTask(task)));
}

async function run (queue:ITask[], maxThreads=0) {
    const exec = new Executor();
    // groupController группирует задачи по ID
    const groupController:Map<number, ITask[]> = new Map();
    // runningTasks хранит активные сессии 
    const runningGroups:ITask[][] = new Array();
    // получаем количество допустимых потоков 
    maxThreads = Math.max(0, maxThreads);
    // функция для дистрибуции потоков 
    // maxThreads === 0 => исполнение без ограничений 
    // получение всех ID-групп и проброс их в executeTask 
    for (const task of queue) {
        // распределение по ID-группам
        if (groupController.has(task.id)) {
            groupController.get(task.id)!.push(task);
        } else {
            groupController.set(task.id, [task]);
        }
    }
    console.log('ID grouping process completed');
    console.log('Executing all the tasks...');
    for (const [k, v] of groupController) {
            runningGroups.push(v);
        } 
    const semaphores: Map<number, Semaphore> = new Map();

    async function process(task: ITask[]) {
        const semaphore = semaphores.get(task[0].id);
        if (!semaphore) {
            semaphores.set(task[0].id, new Semaphore(1));
        }
        await semaphores.get(task[0].id)!.acquire();
        try {
            for (const t of task) {
                await exec.executeTask(t);
            }
        } finally {
            semaphores.get(task[0].id)!.release();
        }
    }

    await Promise.all(runningGroups.map(task => process(task)));
    }


run(Iterable, 3);

// manTestExecutor(Iterable);

// testExecutor();