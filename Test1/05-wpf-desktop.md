# 05 — WPF, XAML & Windows Desktop (zero → interview-ready)

> **Your biggest gap and the JD's most specific requirement (".NET (C#, WPF) — Advanced").**
> Read §1–4 for the model, §5–11 for the questions, §12 to build the app that makes it real.

---

## 1. What WPF actually is (the 90-second version)

WPF (Windows Presentation Foundation, 2006, part of .NET — and **still supported on .NET 8/9/10**,
Windows-only) is a **retained-mode, vector-based, GPU-accelerated** UI framework.

- **Retained mode**: you describe a *tree of objects* (the visual tree); WPF renders it. You don't
  paint pixels in a `WM_PAINT` handler like WinForms/Win32.
- **Vector-based**: resolution-independent; scales cleanly on high-DPI.
- **Rendering**: composed by the **MilCore** render thread on DirectX; your UI thread builds the tree,
  a separate render thread rasterises it.
- **XAML**: declarative markup that is just object construction — `<Button Content="Go"/>` is
  `new Button { Content = "Go" }`.
- **The killer feature**: **data binding + dependency properties**, which make MVVM natural.

**How to describe it vs the web (uses your actual strengths):**
> *"XAML is the view, the view-model is the state, and binding is the reactive glue — the same
> separation as a component + store in Angular or React, except change propagation runs through
> dependency properties and `INotifyPropertyChanged` instead of a virtual DOM or zone.js."*

**WPF vs the alternatives** (be ready — shows currency):
| | WPF | WinForms | WinUI 3 / Windows App SDK | Avalonia | MAUI |
|---|---|---|---|---|---|
| Model | Retained, vector, DirectX | Immediate, GDI+ | Modern successor, Fluent | Cross-platform WPF-alike | Cross-platform mobile+desktop |
| Status | Mature, supported, huge enterprise install base | Legacy but supported | Newer, less mature ecosystem | Popular for cross-platform XAML | Mobile-first |
| Why finance still uses WPF | Data-dense grids, docking layouts, mature 3rd-party controls (DevExpress, Telerik, Syncfusion), 15 yrs of trading-desk apps | | | | |

⚠️ If asked *"is WPF dead?"* → *"It's mature rather than dead — Microsoft still ships it on current
.NET, and for data-dense desktop apps, especially in financial services, the control ecosystem and
the install base make it the pragmatic choice. WinUI 3 is the forward path if you're starting fresh
on Windows, and Avalonia if you need cross-platform XAML."*

---

## 2. The four trees / core object model

```
DependencyObject
 └─ Visual  →  UIElement  →  FrameworkElement  →  Control  →  ContentControl / ItemsControl / Panel
```

- **Logical tree** — the content/structure you wrote in XAML (a `Button` and its content).
- **Visual tree** — the fully expanded tree including every element created by control templates
  (that `Button` is actually a `Border` + `ContentPresenter` + …). You debug with this one; use
  `VisualTreeHelper` / Live Visual Tree in VS.
- Two important consequences: **resource lookup** and **routed events** travel these trees.

---

## 3. Dependency properties (DPs) — the concept interviewers use to test depth

**Q: What is a dependency property and why does WPF need it?**

A property whose value is **not stored in a field on the object** but in a shared, sparse
dictionary-like store keyed by object + property, resolved through a **value-precedence chain**.

Why it exists:
1. **Memory efficiency** — a `Button` has hundreds of properties; storing defaults per instance would
   be enormous. DPs store only values that differ from default.
2. **Value inheritance** — `FontSize` set on a `Window` flows down the tree.
3. **Change notification built in** — binding, animation, styles and triggers all hook the DP system.
4. **Multiple value providers** with a defined precedence.

**Value precedence (highest → lowest)** — worth memorising, it's a classic question:
> **Animation → Local value → Template/Style triggers → Style setters → Theme style → Inheritance → Default**

⚠️ **The famous gotcha:** set a property in code (a *local value*) and it **beats a Style setter and
a data trigger forever** — the trigger appears to "stop working". Fix: `ClearValue()`, or drive it
through the style/binding instead of imperatively.

**Attached property** = a DP defined by one type but set on another, e.g. `Grid.Row="1"` on a
`TextBox`. The `Grid` reads it off its children during layout. `DockPanel.Dock`, `Canvas.Left`,
`Panel.ZIndex` are the same idea.

```csharp
public class GlowBox : Control
{
    public static readonly DependencyProperty PriceProperty =
        DependencyProperty.Register(
            nameof(Price), typeof(decimal), typeof(GlowBox),
            new FrameworkPropertyMetadata(
                0m,
                FrameworkPropertyMetadataOptions.AffectsRender | FrameworkPropertyMetadataOptions.BindsTwoWayByDefault,
                OnPriceChanged));

    public decimal Price { get => (decimal)GetValue(PriceProperty); set => SetValue(PriceProperty, value); }

    private static void OnPriceChanged(DependencyObject d, DependencyPropertyChangedEventArgs e) { /* ... */ }
}
```
⚠️ The CLR wrapper **must** only call `GetValue`/`SetValue` — WPF often bypasses the wrapper and calls
`SetValue` directly, so any logic you put in the setter won't run. Put logic in the change callback.

**DP vs `INotifyPropertyChanged`:** DPs are for **controls** (things that need styling, animation,
inheritance). `INotifyPropertyChanged` is for **view-models** (plain data). Getting this distinction
right is a strong signal.

---

## 4. Data binding — the heart of WPF

```xml
<TextBox Text="{Binding Path=Symbol,
                        Mode=TwoWay,
                        UpdateSourceTrigger=PropertyChanged,
                        Converter={StaticResource UpperConverter},
                        FallbackValue='—',
                        TargetNullValue='(none)',
                        StringFormat='{}{0:N2}',
                        ValidatesOnDataErrors=True}" />
```

**Binding modes:** `OneWay` (source→target), `TwoWay` (both — default for user-editable properties
like `TextBox.Text`), `OneTime`, `OneWayToSource`, `Default`.

**`UpdateSourceTrigger`:** `LostFocus` (default for `TextBox.Text`), `PropertyChanged` (live —
what you want for a search/filter box), `Explicit`.

**Where does the binding look?**
- **`DataContext`** — inherited down the tree; the default source.
- `RelativeSource={RelativeSource AncestorType=Window}` — walk up the visual tree. Essential inside
  `DataTemplate`s where the DataContext is the row item but you need a command on the parent VM.
- `ElementName=otherControl`
- `Source={StaticResource ...}`

**`INotifyPropertyChanged`** — the view-model contract:
```csharp
public class ViewModelBase : INotifyPropertyChanged
{
    public event PropertyChangedEventHandler? PropertyChanged;
    protected bool Set<T>(ref T field, T value, [CallerMemberName] string? name = null)
    {
        if (EqualityComparer<T>.Default.Equals(field, value)) return false;  // suppress no-op churn
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
⚠️ Tricks they check: `[CallerMemberName]` (no magic strings), the **equality guard** (avoids
re-render storms — critical at 20 ticks/sec), raising for **computed/derived** properties, and
`PropertyChanged` with `null`/`string.Empty` name meaning *"everything changed"*.

**`ObservableCollection<T>`** implements `INotifyCollectionChanged` → the UI reacts to
add/remove/move. ⚠️ It does **not** notify when a *property of an item* changes — the item must
implement `INotifyPropertyChanged` itself. This is the #1 WPF beginner bug and a great thing to
mention unprompted.

**Value converters:**
```csharp
public class PnLToBrushConverter : IValueConverter
{
    public object Convert(object value, Type t, object p, CultureInfo c)
        => (decimal)value >= 0 ? Brushes.SeaGreen : Brushes.IndianRed;
    public object ConvertBack(object value, Type t, object p, CultureInfo c) => Binding.DoNothing;
}
```
`IMultiValueConverter` + `MultiBinding` when a target depends on several sources.
⚠️ Converters run on the UI thread for every update — keep them trivial. Prefer a computed VM property
where you can.

**Validation:** `IDataErrorInfo` (older), **`INotifyDataErrorInfo`** (modern, supports async +
multiple errors per property), `ValidationRule`s in XAML, and `Validation.ErrorTemplate` for the
adorner.

---

## 5. MVVM — say it precisely

| Layer | Contains | Knows about |
|---|---|---|
| **Model** | Domain entities, services, data access | Nothing above it |
| **ViewModel** | State + commands + presentation logic. `INotifyPropertyChanged`. **No `using System.Windows.Controls`** | Model |
| **View** | XAML + minimal code-behind. Binds to VM | ViewModel (via `DataContext`) |

**Why MVVM (the real answer):** *testability and designer/developer separation.* The view-model is a
plain class you can unit-test with no UI thread — that's the whole point, and it's the answer to
"why not just use code-behind?"

**Commands** — how the view invokes VM behaviour without code-behind:
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
        add => CommandManager.RequerySuggested += value;      // WPF re-queries automatically
        remove => CommandManager.RequerySuggested -= value;
    }
}
```
`CanExecute` → the button greys out automatically. `CommandManager.InvalidateRequerySuggested()`
forces a re-evaluation.

**Frameworks to name:** **CommunityToolkit.Mvvm** (modern: `[ObservableProperty]`, `[RelayCommand]`
source generators — say you'd use this today), Prism (regions, modularity, `EventAggregator` — very
common in big trading apps), Caliburn.Micro, MVVM Light (retired).

**View↔VM wiring:** `DataContext` set in XAML, or a ViewModelLocator, or DI (`Microsoft.Extensions.
DependencyInjection` in `App.xaml.cs` — modern approach, matches your backend habits).

**How do you show a dialog from a VM without breaking MVVM?** → inject an `IDialogService`. Classic
question; answer instantly.

---

## 6. Layout & controls

**Two-pass layout:** **Measure** (parent asks each child for its desired size given available space)
then **Arrange** (parent assigns final rects). Custom panels override `MeasureOverride`/`ArrangeOverride`.

| Panel | Behaviour |
|---|---|
| `Grid` | Rows/columns; `*` (star = proportional), `Auto`, fixed. The workhorse. |
| `StackPanel` | Stacks; ⚠️ gives children **infinite** space in the stacking direction → **disables UI virtualisation** and breaks scrolling perf |
| `DockPanel` | Dock edges; `LastChildFill` |
| `WrapPanel`, `Canvas`, `UniformGrid` | as named |
| `VirtualizingStackPanel` | Default items panel for `ListBox`/`DataGrid` — creates containers only for visible items |

**Key controls for this role:** `DataGrid` (the trading blotter), `ListView`/`GridView`,
`TreeView`, `TabControl`, `ItemsControl` (+ `DataTemplate`), `ContentControl`.

**Styles vs Templates — the distinction they'll test:**
- **Style** = a set of property setters (+ triggers). Changes *values*.
- **ControlTemplate** = replaces the control's **visual tree** entirely (keeps behaviour). Changes
  *appearance/structure*. Uses `TemplateBinding` to pull from the templated parent.
- **DataTemplate** = how a **data object** is rendered. `DataTemplateSelector` to pick at runtime.
- **Triggers**: `Trigger` (property), `DataTrigger` (bound value), `MultiTrigger`, `EventTrigger`
  (starts storyboards).

**Resources:** `StaticResource` (resolved once at load, faster) vs `DynamicResource` (re-resolved on
change — needed for runtime theming). Lookup walks element → parent → … → `Application.Resources` →
theme. `ResourceDictionary` + `MergedDictionaries` for organisation.

---

## 7. Threading in WPF — **the most likely deep question for this role**

**The rule:** WPF UI objects have **thread affinity**. Only the thread that created a
`DispatcherObject` may touch it. That thread runs a **`Dispatcher`** message loop.

```csharp
// From a background thread:
Application.Current.Dispatcher.Invoke(() => Status = "Connected");         // synchronous, blocks
await Application.Current.Dispatcher.InvokeAsync(() => Status = "Connected"); // preferred
_dispatcher.BeginInvoke(DispatcherPriority.Background, () => { /* low priority */ });
if (_dispatcher.CheckAccess()) { /* already on UI thread */ }
```

**`DispatcherPriority`** matters: `Send` > `Normal` > `DataBind` > `Render` > `Input` > `Background` >
`SystemIdle`. Posting heavy work at `Background` keeps input responsive.

**Freebies WPF gives you:**
- **Binding auto-marshals** simple property updates to the UI thread — so `INotifyPropertyChanged`
  raised from a background thread *usually works*.
- But **collection changes do not**: mutating an `ObservableCollection` from a background thread
  throws `NotSupportedException` ("This type of CollectionView does not support changes to its
  SourceCollection from a different thread"). Two fixes:
  ```csharp
  // 1. Enable collection synchronization (call once, on the UI thread)
  BindingOperations.EnableCollectionSynchronization(_positions, _positionsLock);
  // then mutate from any thread inside lock(_positionsLock) { ... }

  // 2. Or marshal the mutation to the dispatcher
  ```
- `Freezable` objects (brushes, geometries) can be **frozen** → immutable, shareable across threads,
  and faster. `brush.Freeze();` is a real perf tip worth mentioning.

### 🔥 The question to be ready for
> *"You have a market data feed pushing 10,000 price updates per second into a grid of 5,000 rows.
> The UI freezes. What do you do?"*

**Model answer — walk through it in layers:**
1. **Don't touch the UI per tick.** The dispatcher queue floods; the render thread can't keep up; input
   starves. Never `Dispatcher.Invoke` per message.
2. **Conflate.** The screen refreshes at ~60 Hz and a human reads maybe 10 Hz. Keep a
   `ConcurrentDictionary<instrumentId, latestTick>` and **coalesce** — only the newest price per
   instrument matters. Intermediate ticks are discarded.
3. **Batch and flush on a timer.** A `DispatcherTimer` (or a `Channel<T>` consumer) flushes the
   conflated map to the view-models every 100–250 ms, in **one** dispatcher operation.
4. **Only update what changed.** The equality guard in the VM setter suppresses no-op
   `PropertyChanged` events.
5. **Virtualise.** `EnableRowVirtualization` + `EnableColumnVirtualization` on the `DataGrid`,
   `VirtualizationMode="Recycling"` so containers are recycled not recreated. **Never put a
   virtualising items control inside a `StackPanel` or an unconstrained `ScrollViewer`** — it silently
   kills virtualisation.
6. **Update only visible rows** if you go further — off-screen rows don't need refreshing at all.
7. **Reduce visual complexity**: freeze brushes, avoid per-cell converters doing work, avoid deep
   templates, avoid binding to a `DataTable`.
8. **Measure**, don't guess: WPF Performance Suite / Visual Studio's WPF tree + rendering profiler,
   `PresentationTraceSources.TraceLevel=High` for binding errors (silent binding failures are a
   classic hidden cost).
9. **Backpressure policy**: bounded channel, drop-oldest for prices (a stale price is worthless).

That answer alone can carry the WPF portion of the interview. **Learn it.**

---

## 8. Performance checklist (WPF)

- UI + column virtualisation, `VirtualizationMode=Recycling`, `ScrollViewer.CanContentScroll=True`.
- Avoid `StackPanel` as an items panel for long lists.
- `Freeze()` brushes/geometries; share resources via `StaticResource`.
- Reduce visual tree depth; avoid nested `Grid`s where a single grid does.
- `BitmapScalingMode`/`CacheMode="BitmapCache"` for complex static visuals.
- Beware **binding errors** — each one costs an exception + a walk; check the Output window.
- Don't bind to methods/expensive getters; cache computed values.
- `IsAsync=True` or `PriorityBinding` for slow sources.
- Data virtualisation (not just UI virtualisation) for very large sets — load pages on demand.
- Prefer `ItemsSource` over adding items imperatively; use `ICollectionView` for sort/filter/group
  (`CollectionViewSource`) so you don't rebuild collections.

---

## 9. Windows desktop beyond WPF (the "Windows development" must-have)

- **Deployment**: MSI (WiX), ClickOnce, MSIX (modern), or a plain self-contained `dotnet publish`.
  Enterprise trading desks usually push via SCCM/Intune. Know that **auto-update** and
  **side-by-side versioning** are the real problems.
- **Windows Services** / `BackgroundService` with `UseWindowsService()` for the always-on components.
- **Windows authentication**: Kerberos/NTLM, `WindowsIdentity`, integrated auth to SQL Server —
  extremely common in banks. Contrast with OAuth for the web tier (`09`).
- **Registry**, Event Log, Performance Counters, WMI — legacy but present in enterprise Windows apps.
- **Interop**: P/Invoke (`DllImport`), COM interop (Excel automation is huge in finance —
  **know that Excel add-ins/RTD are a common front end for trading data**; name-drop Excel-DNA).
- **Single instance app** via a named `Mutex`.
- **Crash handling**: `AppDomain.CurrentDomain.UnhandledException`,
  `Application.DispatcherUnhandledException`, `TaskScheduler.UnobservedTaskException` — a WPF app
  needs all three wired to logging/telemetry.
- **Clickable killer detail**: WPF apps in banks are often hosted alongside **Excel** and
  **market data APIs (Bloomberg BLPAPI / Refinitiv Eikon)** — see `11`.

---

## 10. Testing WPF

- Unit-test **view-models** (that's the point of MVVM) — no UI thread needed, mock services.
- ⚠️ Tests touching `DispatcherObject`s need an STA thread (`[STAThread]`, `Dispatcher` pumping).
- UI automation: **FlaUI** / White / WinAppDriver / Appium for Windows, or Playwright for the web tier.
- Snapshot/visual regression is harder on desktop — usually manual + smoke tests.
- Testable design: inject `IDialogService`, `IClock`, `IDispatcher` wrapper so tests don't need WPF.

---

## 11. WPF rapid-fire (know all of these)

1. Logical vs visual tree → what you wrote vs what's rendered (templates expanded).
2. `StaticResource` vs `DynamicResource` → load-time once vs re-resolved on change.
3. `x:Name` vs `Name` → XAML namescope field vs the `FrameworkElement.Name` DP (mostly equivalent).
4. Routed events → **bubbling** (up), **tunnelling** (`Preview*`, down), direct. `e.Handled = true`
   stops it.
5. `ContentControl` vs `ItemsControl` → one item vs many.
6. `DataTemplate` vs `ControlTemplate` → how *data* looks vs how a *control* looks.
7. `TemplateBinding` vs `Binding RelativeSource TemplatedParent` → lightweight one-way inside a
   template vs full binding (needed for two-way/converters).
8. `ICollectionView` → sorting/filtering/grouping/current-item over a collection without copying it.
9. `IValueConverter` vs `IMultiValueConverter` → one source vs several.
10. `Dispatcher` vs `SynchronizationContext` → WPF's message pump vs the general abstraction async uses.
11. Why does my binding silently do nothing? → wrong `DataContext`, typo in path (bindings fail
    silently), missing `INotifyPropertyChanged`, or a local value overriding. Check the Output window.
12. Memory leaks in WPF → **event handlers** (use `WeakEventManager`), `DispatcherTimer` holding the
    VM alive, static resources, `CommandManager.RequerySuggested` (weak, but a classic suspect),
    bindings to long-lived sources. Diagnose with dotMemory/VS heap snapshots.
13. `Freezable` → immutable, thread-shareable, faster.
14. Attached behaviour → attached property that wires up event handlers, so you keep code-behind empty.
15. `x:Static`, `x:Type`, `x:Null`, `x:Array` → markup extensions.
16. Virtualisation types → UI virtualisation (containers) vs data virtualisation (the data itself).

---

## 12. 🔨 BUILD THIS SATURDAY — 2.5 hours, and you can speak from experience

**Spec:** a real-time positions blotter. This is *deliberately* the same shape as the system they're
hiring for.

```
dotnet new wpf -n TradingBlotter
cd TradingBlotter
dotnet add package CommunityToolkit.Mvvm
dotnet run
```

**Build it in this order — each step maps to interview questions:**

| Step | Build | Teaches you |
|---|---|---|
| 1 | `Position` model + `PositionViewModel : ObservableObject` with `Symbol, Qty, Avg, Last, PnL` | `INotifyPropertyChanged`, computed properties, equality guards |
| 2 | `MainViewModel` with `ObservableCollection<PositionViewModel>`, seed 5,000 rows | `ObservableCollection`, `DataContext` |
| 3 | `DataGrid` bound to it, `AutoGenerateColumns=False`, explicit columns, `StringFormat='{}{0:N2}'` | Binding, string formatting |
| 4 | A `PnLToBrushConverter` colouring P&L red/green | `IValueConverter`, resources |
| 5 | A background `Task`/`Thread` generating random ticks 20×/sec for random symbols | Threading |
| 6 | **Naively** push each tick straight to the VM → watch it stutter | Feel the problem |
| 7 | Fix it: `Channel<Tick>` + `ConcurrentDictionary` conflation + `DispatcherTimer` flush every 150 ms | **The §7 answer, lived** |
| 8 | `EnableRowVirtualization="True"`, `VirtualizationMode="Recycling"` | Virtualisation |
| 9 | Filter `TextBox` bound with `UpdateSourceTrigger=PropertyChanged` driving an `ICollectionView.Filter` | `ICollectionView`, live filtering |
| 10 | A `RelayCommand` "Pause feed" button with `CanExecute` | Commands |
| 11 | Deliberately break a binding, find the error in the Output window | Debugging bindings |
| 12 | Wire DI in `App.xaml.cs` with `Microsoft.Extensions.DependencyInjection` | Modern WPF composition |

**Then write down, in your own words, three sentences about what surprised you.** Those three
sentences are what make your WPF answer sound lived rather than read — and they're what you'll say in
the §5.1 script in `02`.

**Starter for step 7 (the important one):**
```csharp
private readonly ConcurrentDictionary<string, decimal> _pending = new();
private readonly DispatcherTimer _flush = new() { Interval = TimeSpan.FromMilliseconds(150) };

void OnTick(Tick t) => _pending[t.Symbol] = t.Price;      // conflate: newest wins, no UI touch

void Start()
{
    _flush.Tick += (_, _) =>
    {
        foreach (var kv in _pending)
            if (_bySymbol.TryGetValue(kv.Key, out var vm))
                vm.Last = kv.Value;      // equality guard inside suppresses no-op notifications
        _pending.Clear();
    };
    _flush.Start();
}
```
