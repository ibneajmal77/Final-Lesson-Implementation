# 05 — WPF & WINDOWS DESKTOP, IN PLAIN ENGLISH

> **Your biggest gap, and the job's most specific requirement: ".NET (C#, WPF) — Advanced".**
>
> Read **Part 0** and **Part 7** first. Part 7 alone can carry the WPF portion of the interview.
>
> **Format:** **Q:** what they ask → **Say:** the words you speak → **Remember:** the hook.

---

# FULL TECH LOAD MEMORY HOOKS

Use these as labels for the full detail below. Say the hook first, then expand only where the
interviewer pushes.

| Hook | Simple wording | Full tech load to keep |
|---|---|---|
| **Retained tree** | You describe objects; WPF renders them. | Visual tree, logical tree, templates, GPU composition, high-DPI vector UI. |
| **XAML builds objects** | Markup is object construction. | XAML maps to CLR objects, properties, resources, bindings, templates. |
| **DPs are shared storage** | Controls do not store every property in fields. | Sparse property store, inheritance, notification, animation, styling, value precedence. |
| **Local beats style** | Code-set values override triggers. | DP precedence: animation, local value, template/style triggers, setters, inherited, default; fix with `ClearValue()`. |
| **VMs notify, controls depend** | View-models use `INotifyPropertyChanged`; controls use DPs. | MVVM boundary, testability, no `System.Windows.Controls` in view-models. |
| **Collection is not item** | `ObservableCollection` reports add/remove, not row field changes. | Item types need `INotifyPropertyChanged`; computed properties need manual raises. |
| **Dispatcher owns UI** | Only the UI thread touches WPF objects. | Thread affinity, `Dispatcher.InvokeAsync`, `DispatcherTimer`, background work, cancellation. |
| **Conflate, batch, flush** | Never update the grid per tick. | Latest per instrument, bounded channel, timer flush, equality guard, virtualization with recycling. |
| **Virtualize or freeze** | Big grids need fewer visual objects. | Recycling, shallow visual tree, frozen brushes/geometries, binding error tracing. |

---

# PART 0 — THE 10 WPF ANSWERS THAT WIN

| # | The question | The answer, in one breath |
|---|---|---|
| 1 | **What is WPF?** | "A retained-mode, vector-based, GPU-composed UI framework. I describe a tree of objects and WPF renders it — I never paint pixels. XAML is just object construction." |
| 2 | **The killer feature** | "Data binding plus dependency properties. That's what makes MVVM natural." |
| 3 | **Dependency property — why?** | "Values aren't stored in a field per instance. They're in a shared store with a precedence chain — so you get low memory, value inheritance, built-in change notification, and multiple value providers." |
| 4 | **The famous DP gotcha** | "**A local value set in code beats a style trigger, forever.** That's why 'my trigger stopped working'. Fix with `ClearValue()`, or drive it through the style instead." |
| 5 | **DP vs `INotifyPropertyChanged`** | "Dependency properties are for **controls**. `INotifyPropertyChanged` is for **view-models**. Getting that split right is the signal." |
| 6 | **The `ObservableCollection` trap** | "It notifies about **add and remove**, not about a property changing **inside** an item. The item must implement `INotifyPropertyChanged` itself. The number one WPF beginner bug." |
| 7 | **Why MVVM?** | "**Testability.** The view-model is a plain class I can unit-test with no UI thread. That's the whole point, and it's the answer to 'why not code-behind?'" |
| 8 | **UI thread rule** | "WPF objects have **thread affinity** — only the creating thread may touch them. Background work marshals through the `Dispatcher`." |
| 9 | **10,000 ticks/sec into a 5,000-row grid** | "Don't touch the UI per tick. **Conflate → batch → flush on a timer → equality guard → virtualise with recycling → bounded channel, drop oldest.**" |
| 10 | **Dialog from a view-model?** | "Inject an `IDialogService`. Instantly — it's a classic question." |

---

# PART 1 — WHAT WPF ACTUALLY IS

**Say (the 60-second version):**

> *"WPF is a **retained-mode, vector-based, GPU-accelerated** UI framework, still supported on
> .NET 8, 9 and 10 — Windows-only.*
>
> - ***Retained mode*** *means I describe a tree of objects — the visual tree — and WPF renders it.
>   I never paint pixels in a paint handler the way you do in WinForms or Win32.*
> - ***Vector-based*** *means it's resolution-independent and scales cleanly on high-DPI.*
> - ***XAML*** *is declarative markup that's really just object construction —* `<Button Content="Go"/>`
>   *is* `new Button { Content = "Go" }`.
> - ***And the killer feature is data binding plus dependency properties***, *which is what makes MVVM
>   natural."*

**The comparison that uses your actual strength — say it:**
> *"XAML is the view, the view-model is the state, and binding is the reactive glue. It's the same
> separation as a component plus a store in React or Angular — except change propagation runs through
> dependency properties and `INotifyPropertyChanged` instead of a virtual DOM."*

## Is WPF dead?

**Say:** *"It's mature rather than dead. Microsoft still ships it on current .NET, and for data-dense
desktop apps — especially in financial services — the third-party control ecosystem and the install
base make it the pragmatic choice. WinUI 3 is the forward path if you're starting fresh on Windows,
and Avalonia if you need cross-platform XAML."*

**Why finance still uses it:** data-dense grids, docking layouts, mature commercial controls
(DevExpress, Telerik, Syncfusion), and fifteen years of trading-desk apps already built on it.

---

# PART 2 — THE TWO TREES

```
DependencyObject
 └─ Visual → UIElement → FrameworkElement → Control → ContentControl / ItemsControl / Panel
```

- **Logical tree** — the structure you actually wrote in XAML.
- **Visual tree** — the fully expanded tree, including everything created by control templates. A
  `Button` is really a `Border` plus a `ContentPresenter` plus more. **This is the one you debug with**
  — `VisualTreeHelper`, or the Live Visual Tree in Visual Studio.

**Why it matters:** **resource lookup** and **routed events** both travel these trees.

---

# PART 3 — DEPENDENCY PROPERTIES

**Q: What is a dependency property, and why does WPF need it?**

**Say:** *"It's a property whose value isn't stored in a field on the object. It lives in a shared,
sparse store keyed by object and property, and it's resolved through a **value precedence chain**.*

*There are four reasons it exists:*
1. ***Memory.*** *A `Button` has hundreds of properties. Storing every default on every instance would
   be enormous — DPs only store values that differ from the default.*
2. ***Value inheritance.*** *`FontSize` set on the `Window` flows down the whole tree.*
3. ***Change notification is built in*** *— binding, animation, styles and triggers all hook into it.*
4. ***Multiple value providers*** *with a defined precedence order."*

## The precedence chain — memorise this, it's a classic question

> **Animation → Local value → Template/Style triggers → Style setters → Theme style → Inheritance → Default**

⚠️ **The famous gotcha, and it's worth raising unprompted:**

**Say:** *"Set a property in code and that's a **local value**, which beats a style setter and a data
trigger **forever**. That's why people say 'my trigger stopped working' — it never fired because a
local value outranks it. The fix is `ClearValue()`, or driving it through the style or a binding
instead of setting it imperatively."*

## Attached properties

**Say:** *"An attached property is a DP defined by one type but set on another — `Grid.Row="1"` on a
`TextBox`. The `Grid` reads it off its children during layout. `DockPanel.Dock`, `Canvas.Left` and
`Panel.ZIndex` are all the same idea."*

```csharp
public static readonly DependencyProperty PriceProperty =
    DependencyProperty.Register(
        nameof(Price), typeof(decimal), typeof(GlowBox),
        new FrameworkPropertyMetadata(
            0m,
            FrameworkPropertyMetadataOptions.AffectsRender,
            OnPriceChanged));

public decimal Price { get => (decimal)GetValue(PriceProperty); set => SetValue(PriceProperty, value); }
```

⚠️ **The detail that shows depth:** *"The CLR wrapper must only call `GetValue` and `SetValue`. WPF
frequently bypasses the wrapper and calls `SetValue` directly, so any logic you put in the setter
simply won't run. Logic goes in the change callback."*

## DP vs `INotifyPropertyChanged`

**Say:** *"Dependency properties are for **controls** — things that need styling, animation and value
inheritance. `INotifyPropertyChanged` is for **view-models**, which are plain data. Getting that
distinction right is what separates someone who's used WPF from someone who's read about it."*

---

# PART 4 — DATA BINDING

```xml
<TextBox Text="{Binding Path=Symbol,
                        Mode=TwoWay,
                        UpdateSourceTrigger=PropertyChanged,
                        Converter={StaticResource UpperConverter},
                        FallbackValue='—',
                        StringFormat='{}{0:N2}'}" />
```

**Binding modes:** `OneWay` (source → target) · `TwoWay` (both — the default for user-editable things
like `TextBox.Text`) · `OneTime` · `OneWayToSource`.

**`UpdateSourceTrigger`:** `LostFocus` (default for `TextBox.Text`) · **`PropertyChanged`** (live —
what you want for a search or filter box) · `Explicit`.

**Where does a binding look for its source?**
- **`DataContext`** — inherited down the tree. The default.
- `RelativeSource={RelativeSource AncestorType=Window}` — walk up the visual tree. **Essential inside
  a `DataTemplate`**, where the DataContext is the row item but the command lives on the parent VM.
- `ElementName=otherControl`
- `Source={StaticResource ...}`

## `INotifyPropertyChanged` — the view-model contract

```csharp
public class ViewModelBase : INotifyPropertyChanged
{
    public event PropertyChangedEventHandler? PropertyChanged;

    protected bool Set<T>(ref T field, T value, [CallerMemberName] string? name = null)
    {
        if (EqualityComparer<T>.Default.Equals(field, value)) return false;   // the equality guard
        field = value;
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
        return true;
    }
}

public class PositionViewModel : ViewModelBase
{
    private decimal _last;
    public decimal Last { get => _last; set { if (Set(ref _last, value)) OnPropertyChanged(nameof(PnL)); } }
    public decimal PnL => (Last - Avg) * Qty;      // computed — must be raised manually
}
```

⚠️ **Four things they check here:**
1. `[CallerMemberName]` — no magic strings.
2. **The equality guard.** *"This is what stops a re-render storm at 20 ticks a second — if the value
   didn't actually change, don't raise the event."*
3. Raising for **computed** properties like `PnL`, which nothing else will notice.
4. `PropertyChanged` with a `null` or empty name means **"everything changed"**.

## `ObservableCollection<T>` — the number one trap

**Say:** *"It implements `INotifyCollectionChanged`, so the UI reacts to items being **added, removed
or moved**. But it does **not** notify when a **property inside an item** changes — the item itself
has to implement `INotifyPropertyChanged`. That's the most common WPF beginner bug, and it's worth
mentioning before they ask."*

## Value converters

```csharp
public class PnLToBrushConverter : IValueConverter
{
    public object Convert(object value, Type t, object p, CultureInfo c)
        => (decimal)value >= 0 ? Brushes.SeaGreen : Brushes.IndianRed;
    public object ConvertBack(object value, Type t, object p, CultureInfo c) => Binding.DoNothing;
}
```

⚠️ *"Converters run on the UI thread for every single update, so I keep them trivial. Where I can,
I'd rather have a computed property on the view-model."*

`IMultiValueConverter` + `MultiBinding` when the target depends on several sources.

**Validation:** `IDataErrorInfo` (older) · **`INotifyDataErrorInfo`** (modern — supports async and
multiple errors per property) · `ValidationRule` in XAML · `Validation.ErrorTemplate` for the adorner.

---

# PART 5 — MVVM

| Layer | Contains | Knows about |
|---|---|---|
| **Model** | Domain entities, services, data access | Nothing above it |
| **ViewModel** | State, commands, presentation logic. `INotifyPropertyChanged`. **No `System.Windows.Controls`** | The Model |
| **View** | XAML plus minimal code-behind | The ViewModel, via `DataContext` |

**Q: Why MVVM, and not just code-behind?**
**Say:** *"Testability, and designer/developer separation. The view-model is a plain class I can unit
test with no UI thread and no XAML. That's the whole point."*

## Commands — how the view calls the view-model without code-behind

```csharp
public class RelayCommand : ICommand
{
    private readonly Action<object?> _execute;
    private readonly Predicate<object?>? _canExecute;

    public RelayCommand(Action<object?> execute, Predicate<object?>? canExecute = null)
        => (_execute, _canExecute) = (execute, canExecute);

    public bool CanExecute(object? p) => _canExecute?.Invoke(p) ?? true;
    public void Execute(object? p) => _execute(p);

    public event EventHandler? CanExecuteChanged
    {
        add    => CommandManager.RequerySuggested += value;   // WPF re-queries automatically
        remove => CommandManager.RequerySuggested -= value;
    }
}
```

**Say:** *"`CanExecute` returning false greys the button out automatically — I don't write any code to
enable or disable it. `CommandManager.InvalidateRequerySuggested()` forces a re-evaluation."*

**Frameworks to name:**
- **CommunityToolkit.Mvvm** — modern. `[ObservableProperty]` and `[RelayCommand]` source generators.
  **Say you'd use this today.**
- **Prism** — regions, modularity, `EventAggregator`. **Very common in big trading apps** — worth
  naming for this role specifically.
- Caliburn.Micro. MVVM Light is retired.

**Q: How do you show a dialog from a view-model without breaking MVVM?**
**Say:** *"Inject an `IDialogService`. The view-model asks for a decision; the implementation knows
about windows. The view-model stays testable."* **Answer this one instantly — it's a classic.**

---

# PART 6 — LAYOUT, STYLES, TEMPLATES

**Two-pass layout:** **Measure** (the parent asks each child how big it wants to be, given the
available space), then **Arrange** (the parent assigns final rectangles). Custom panels override
`MeasureOverride` and `ArrangeOverride`.

| Panel | Behaviour |
|---|---|
| `Grid` | Rows and columns. `*` proportional, `Auto`, or fixed. The workhorse |
| `StackPanel` | Stacks. ⚠️ **Gives children infinite space in the stacking direction, which disables UI virtualisation** |
| `DockPanel` | Dock to edges; `LastChildFill` |
| `VirtualizingStackPanel` | The default items panel for `ListBox` and `DataGrid` — creates containers only for visible rows |

## Styles vs templates — the distinction they'll test

**Say:**
- *"A **Style** is a set of property setters plus triggers. It changes **values**."*
- *"A **ControlTemplate** replaces the control's entire visual tree while keeping its behaviour. It
  changes **appearance and structure**. It uses `TemplateBinding` to pull values from the templated
  parent."*
- *"A **DataTemplate** says how a **data object** should be rendered. `DataTemplateSelector` picks one
  at runtime."*

**Triggers:** `Trigger` (on a property) · `DataTrigger` (on a bound value) · `MultiTrigger` ·
`EventTrigger` (starts a storyboard).

**Resources:** `StaticResource` is resolved once at load and is faster. `DynamicResource` is
re-resolved when it changes — needed for runtime theming. Lookup walks element → parent → … →
`Application.Resources` → theme.

---

# PART 7 — 🔥 THREADING IN WPF (the most likely deep question)

## 7.1 The rule

**Say:** *"WPF UI objects have **thread affinity**. Only the thread that created a `DispatcherObject`
may touch it, and that thread runs a `Dispatcher` message loop. Anything on a background thread has to
marshal through the dispatcher."*

```csharp
Application.Current.Dispatcher.Invoke(() => Status = "Connected");        // synchronous, blocks
await Application.Current.Dispatcher.InvokeAsync(() => Status = "OK");    // preferred
_dispatcher.BeginInvoke(DispatcherPriority.Background, () => { /* low priority */ });
if (_dispatcher.CheckAccess()) { /* already on the UI thread */ }
```

**`DispatcherPriority` matters:** `Send` > `Normal` > `DataBind` > `Render` > `Input` > `Background` >
`SystemIdle`. Posting heavy work at `Background` keeps input responsive.

## 7.2 What WPF gives you for free — and what it doesn't

**Say:** *"Binding **auto-marshals** simple property updates to the UI thread, so raising
`PropertyChanged` from a background thread usually just works.*

*But **collection changes do not**. Mutating an `ObservableCollection` from a background thread throws
`NotSupportedException`. Two fixes: `BindingOperations.EnableCollectionSynchronization` with a lock
object, or marshal the mutation onto the dispatcher."*

```csharp
BindingOperations.EnableCollectionSynchronization(_positions, _positionsLock);   // once, on the UI thread
// then mutate from any thread inside lock(_positionsLock) { ... }
```

**`Freezable`:** *"Brushes and geometries can be **frozen** — that makes them immutable, shareable
across threads, and faster. `brush.Freeze()` is a real, cheap performance win."*

---

## 7.3 🔥 THE QUESTION TO BE READY FOR

> *"You have a market data feed pushing **10,000 price updates a second** into a grid of **5,000
> rows**. The UI freezes. What do you do?"*

**Walk through it in layers. This answer alone can carry the WPF portion of the interview.**

**1. Don't touch the UI per tick.**
*"The dispatcher queue floods, the render thread can't keep up, and input starves. Never
`Dispatcher.Invoke` per message."*

**2. Conflate.**
*"The screen refreshes at about 60 Hz and a human reads maybe 10. So I keep a
`ConcurrentDictionary<instrument, latestTick>` and coalesce — only the newest price per instrument
matters. Every intermediate tick is discarded, and that's correct, not a compromise."*

**3. Batch and flush on a timer.**
*"A `DispatcherTimer` — or a `Channel<T>` consumer — flushes the conflated map to the view-models
every 100 to 250 milliseconds, in **one** dispatcher operation instead of ten thousand."*

**4. Only update what actually changed.**
*"The equality guard in the view-model setter suppresses no-op `PropertyChanged` events."*

**5. Virtualise.**
*"`EnableRowVirtualization` and `EnableColumnVirtualization` on the `DataGrid`, with
`VirtualizationMode="Recycling"` so containers are recycled rather than recreated. And **never** put a
virtualising items control inside a `StackPanel` or an unconstrained `ScrollViewer`** — it silently
kills virtualisation and nothing tells you."*

**6. Reduce visual work.**
*"Freeze brushes, keep converters trivial, avoid deep templates."*

**7. Measure, don't guess.**
*"The WPF profiler, and `PresentationTraceSources.TraceLevel=High` for binding errors — silent binding
failures are a classic hidden cost, because each one is an exception plus a tree walk."*

**8. Set a backpressure policy.**
*"A bounded channel, drop-oldest, because a stale price is worthless. For orders I'd never drop."*

**Remember the chain: conflate → batch → flush on a timer → equality guard → virtualise → bounded channel.**

---

# PART 8 — WPF PERFORMANCE CHECKLIST

- UI **and** column virtualisation, `VirtualizationMode=Recycling`, `CanContentScroll=True`.
- **Never** a `StackPanel` as the items panel for a long list.
- `Freeze()` brushes and geometries. Share resources with `StaticResource`.
- Keep the visual tree shallow — avoid nested `Grid`s where one will do.
- **Watch the Output window for binding errors.** Each one costs an exception plus a tree walk.
- Don't bind to expensive getters or methods — cache the computed value.
- `IsAsync=True` or `PriorityBinding` for slow sources.
- **Data** virtualisation (not just UI virtualisation) for very large sets — load pages on demand.
- Use `ICollectionView` / `CollectionViewSource` for sort, filter and group, so you never rebuild the
  collection.

---

# PART 9 — WINDOWS DEVELOPMENT BEYOND WPF

The job lists **"Windows development"** as a must-have. Cover this ground:

- **Deployment:** MSI (WiX), ClickOnce, **MSIX** (modern), or a self-contained `dotnet publish`.
  Enterprise desks usually push via SCCM or Intune. **The real problems are auto-update and
  side-by-side versioning** — say that, it shows you've shipped desktop software.
- **Windows Services** — `BackgroundService` with `UseWindowsService()` for always-on components.
- **Windows authentication** — Kerberos and NTLM, `WindowsIdentity`, integrated auth to SQL Server.
  **Extremely common in banks.** Contrast with OAuth for the web tier (`09`).
- **Interop** — P/Invoke via `DllImport`, and COM interop. ⚠️ **Excel automation is huge in finance.**
  Know that **Excel add-ins and RTD are a very common front end for trading data**, and name-drop
  **Excel-DNA**. That single detail sounds like domain experience.
- **Single instance** — a named `Mutex`.
- **Crash handling** — a WPF app needs **all three** wired to logging:
  `AppDomain.CurrentDomain.UnhandledException`, `Application.DispatcherUnhandledException`, and
  `TaskScheduler.UnobservedTaskException`.
- Registry, Event Log, performance counters, WMI — legacy but present in enterprise Windows apps.

---

# PART 10 — TESTING WPF

- **Unit-test the view-models.** That's the point of MVVM — no UI thread needed, mock the services.
- ⚠️ Tests touching `DispatcherObject`s need an STA thread.
- **UI automation:** FlaUI, WinAppDriver, or Appium for Windows.
- **Design for testability:** inject `IDialogService`, `IClock`, and a dispatcher wrapper, so the
  tests never need WPF at all.

---

# PART 11 — RAPID-FIRE: 30 QUESTIONS

| # | Q | A |
|---|---|---|
| 1 | Logical vs visual tree | What you wrote vs what's rendered, with templates expanded |
| 2 | What is XAML? | Declarative object construction — `<Button/>` is `new Button()` |
| 3 | Retained mode | You describe a tree; WPF renders it. You never paint pixels |
| 4 | Why dependency properties? | Memory, value inheritance, built-in change notification, multiple providers |
| 5 | DP precedence order | Animation → local → triggers → style → theme → inherited → default |
| 6 | Why did my trigger stop working? | A **local value** set in code outranks it forever |
| 7 | Attached property | A DP defined by one type, set on another — `Grid.Row` |
| 8 | DP vs `INotifyPropertyChanged` | Controls vs view-models |
| 9 | `StaticResource` vs `DynamicResource` | Resolved once at load vs re-resolved on change |
| 10 | `x:Name` vs `Name` | XAML namescope field vs the `FrameworkElement.Name` property |
| 11 | Routed events | **Bubbling** up, **tunnelling** down (`Preview*`), or direct. `e.Handled` stops it |
| 12 | `ContentControl` vs `ItemsControl` | One item vs many |
| 13 | `DataTemplate` vs `ControlTemplate` | How **data** looks vs how a **control** looks |
| 14 | `TemplateBinding` | Lightweight one-way binding inside a template |
| 15 | Binding modes | OneWay, TwoWay, OneTime, OneWayToSource |
| 16 | `UpdateSourceTrigger` | `LostFocus` default; `PropertyChanged` for live filters |
| 17 | `ObservableCollection` limit | Notifies add/remove — **not** property changes inside items |
| 18 | Equality guard, why? | Stops a re-render storm at high tick rates |
| 19 | `[CallerMemberName]` | No magic strings in `PropertyChanged` |
| 20 | `ICollectionView` | Sort, filter, group and current-item, without copying the collection |
| 21 | `IValueConverter` vs Multi | One source vs several |
| 22 | Why MVVM? | Testability — the view-model is a plain testable class |
| 23 | Dialog from a VM? | Inject an `IDialogService` |
| 24 | `ICommand` / `CanExecute` | Greys the button out automatically |
| 25 | UI thread rule | Thread affinity — marshal through the `Dispatcher` |
| 26 | Background collection edits | `BindingOperations.EnableCollectionSynchronization` |
| 27 | `Freezable` | Immutable, shareable across threads, faster |
| 28 | Silent binding failure | Wrong DataContext, typo'd path, missing INPC. **Check the Output window** |
| 29 | WPF memory leaks | **Event handlers** (`WeakEventManager`), `DispatcherTimer`, static resources |
| 30 | Virtualisation types | **UI** virtualisation (containers) vs **data** virtualisation (the data itself) |

---

# PART 12 — 🔨 THE 2-HOUR BUILD (do this if you have any time at all)

**Why:** you cannot credibly claim "Advanced WPF" from reading. But after building this you can
honestly say *"I've been hands-on in WPF recently, building a real-time positions grid"* — and answer
twenty questions from **lived experience** instead of theory.

```
dotnet new wpf -n TradingBlotter
cd TradingBlotter
dotnet add package CommunityToolkit.Mvvm
dotnet run
```

**Build in this order. Each step maps directly to an interview question.**

| Step | Build | Teaches you |
|---|---|---|
| 1 | `PositionViewModel : ObservableObject` with `Symbol, Qty, Avg, Last, PnL` | `INotifyPropertyChanged`, computed properties, equality guards |
| 2 | `MainViewModel` with an `ObservableCollection`, seeded with 5,000 rows | `ObservableCollection`, `DataContext` |
| 3 | `DataGrid` bound to it, explicit columns, `StringFormat='{}{0:N2}'` | Binding and formatting |
| 4 | A `PnLToBrushConverter` colouring P&L red and green | `IValueConverter`, resources |
| 5 | A background task generating random ticks 20 times a second | Threading |
| 6 | **Naively** push every tick straight to the VM → **watch it stutter** | **Feel the problem** |
| 7 | Fix it: conflate in a `ConcurrentDictionary` + flush on a `DispatcherTimer` every 150 ms | **The Part 7 answer, lived** |
| 8 | Turn on row virtualisation with `VirtualizationMode="Recycling"` | Virtualisation |
| 9 | A filter `TextBox` with `UpdateSourceTrigger=PropertyChanged` driving `ICollectionView.Filter` | Live filtering |
| 10 | A `RelayCommand` "Pause feed" button with `CanExecute` | Commands |
| 11 | Deliberately break a binding, find it in the Output window | Debugging bindings |

**Step 7 is the important one — this is the code:**
```csharp
private readonly ConcurrentDictionary<string, decimal> _pending = new();
private readonly DispatcherTimer _flush = new() { Interval = TimeSpan.FromMilliseconds(150) };

void OnTick(Tick t) => _pending[t.Symbol] = t.Price;      // conflate — newest wins, no UI touch

void Start()
{
    _flush.Tick += (_, _) =>
    {
        foreach (var kv in _pending)
            if (_bySymbol.TryGetValue(kv.Key, out var vm))
                vm.Last = kv.Value;          // the equality guard inside suppresses no-ops
        _pending.Clear();
    };
    _flush.Start();
}
```

**Then write down three sentences about what surprised you.** Those three sentences are what make your
WPF answer sound **lived rather than read** — and they're the strongest thing you can bring to this
interview on WPF.

**If you have no time to build:** say so honestly, and lean on the Part 7 answer plus your
`INotifyPropertyChanged` ↔ React/Angular binding comparison. **Never bluff on WPF.** In a
capital-markets interview the person opposite you has shipped WPF for a decade.
