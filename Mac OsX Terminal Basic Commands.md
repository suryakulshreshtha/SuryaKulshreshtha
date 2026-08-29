# ⌨️ Xcode Keyboard Shortcuts

A working reference for Xcode. Originally written around Xcode 6–8; the **Legacy** column flags the handful of bindings Apple has since moved, so an old muscle-memory habit doesn't send you somewhere unexpected.

**Modifier keys** — `⌘` Command · `⌥` Option · `⌃` Control · `⇧` Shift · `↩` Return · `⇥` Tab

[General](#general) · [Build--run](#build--run) · [Code navigation](#code-navigation) · [Code editing](#code-editing) · [File navigation](#file-navigation) · [Debugging](#debugging) · [Panes--libraries](#panes--libraries) · [Refactoring](#refactoring) · [SwiftUI](#swiftui-previews)

---

## General

| Action | Shortcut |
|---|---|
| Preferences / Settings | `⌘,` |
| Documentation window | `⇧⌘0` |
| Quick Help for symbol under cursor | `⌘?` |
| Documentation for selected text | `⌃⌘?` |
| Activate console | `⇧⌘C` |
| Clear console | `⌘K` |

---

## Build & Run

| Action | Shortcut |
|---|---|
| Build | `⌘B` |
| Run | `⌘R` |
| Stop | `⌘.` |
| Test | `⌘U` |
| Profile (Instruments) | `⌘I` |
| Analyze | `⇧⌘B` |
| Clean build folder | `⇧⌘K` |
| Build & run without building again | `⌃⌘R` |

> 💡 Hold `⌥` while clicking **Run** to open the scheme options sheet instead of launching.

---

## Code Navigation

### Within a line or file

| Action | Shortcut |
|---|---|
| Beginning of line | `⌘←` |
| End of line | `⌘→` |
| Top of file | `⌘↑` |
| Bottom of file | `⌘↓` |
| Next / previous word | `⌥→` / `⌥←` |
| Next / previous subword | `⌃→` / `⌃←` |
| Centre selection in view | `⌃L` |
| Go to line… | `⌘L` |

Add `⇧` to any movement above to extend the selection instead of moving the caret.

### Finding things

| Action | Shortcut |
|---|---|
| Find in file | `⌘F` |
| Find & replace in file | `⌥⌘F` |
| Find in project | `⇧⌘F` |
| Find & replace in project | `⌥⇧⌘F` |
| Find next / previous | `⌘G` / `⇧⌘G` |
| Jump to definition | `⌃⌘J` |
| Jump to next counterpart (`.h` ⇄ `.m`, view ⇄ model) | `⌃⌘↑` / `⌃⌘↓` |

---

## Code Editing

| Action | Shortcut |
|---|---|
| Show completions | `⌃Space` |
| Next completion | `⌃.` |
| Accept completion | `⇥` |
| Next / previous placeholder | `⌃/` / `⇧⌃/` |
| Comment / uncomment selection | `⌘/` |
| Fold method or class | `⌥⌘←` |
| Unfold method or class | `⌥⌘→` |
| Fold / unfold all methods | `⌥⇧⌘←` / `⌥⇧⌘→` |
| Edit all in scope (rename locally) | `⌃⌘E` |
| Re-indent selection | `⌃I` |
| Move line up / down | `⌥⌘[` / `⌥⌘]` |
| Duplicate line | `⌘D` |
| Delete line | `⌘⌫` |
| Add cursor above / below | `⌃⇧↑` / `⌃⇧↓` |

---

## File Navigation

| Action | Shortcut |
|---|---|
| Open Quickly (fuzzy file/symbol search) | `⇧⌘O` |
| Go back / forward through history | `⌃⌘←` / `⌃⌘→` |
| Show related items menu | `⌃1` |
| Recent files menu | `⌃2` |
| Jump bar for the current file | `⌃6` |
| Close editor pane | `⌃⇧⌘W` |
| Open file in assistant editor | `⌥` + click |

---

## Debugging

| Action | Shortcut |
|---|---|
| Add breakpoint at current line | `⌘\` |
| Activate / deactivate all breakpoints | `⌘Y` |
| Breakpoint navigator | `⌘7` |
| Step over | `F6` |
| Step into | `F7` |
| Step out | `F8` |
| Continue | `⌃⌘Y` |
| Show / hide debug area | `⇧⌘Y` |
| Next issue | `⌘'` |
| Previous issue | `⌘"` |
| Fix next issue | `⌃⌘'` |
| Fix previous issue | `⌃⌘"` |

---

## Panes & Libraries

| Action | Shortcut | Legacy note |
|---|---|---|
| Show / hide navigator (left) | `⌘0` | |
| Navigator tabs 1–9 | `⌘1` … `⌘9` | |
| Show / hide inspector (right) | `⌥⌘0` | |
| Inspector tabs | `⌥⌘1` … `⌥⌘7` | |
| Show / hide debug area | `⇧⌘Y` | |
| **Library** (snippets, objects, media, all in one) | `⇧⌘L` | Replaced the four separate palettes below in Xcode 11 |
| File template library | `⌃⌥⌘1` | Xcode ≤ 10 |
| Code snippet library | `⌃⌥⌘2` | Xcode ≤ 10 |
| Object library | `⌃⌥⌘3` | Xcode ≤ 10 |
| Media library | `⌃⌥⌘4` | Xcode ≤ 10 |

---

## Refactoring

| Action | Shortcut |
|---|---|
| Rename symbol project-wide | `⌃⌘E`, or `⌘` + click → **Rename** |
| Extract to method / variable | `⌘` + click → **Refactor** |
| Show refactoring menu | `⌘` + click on symbol |

---

## SwiftUI Previews

| Action | Shortcut |
|---|---|
| Resume preview canvas | `⌥⌘P` |
| Show / hide canvas | `⌥⌘↩` |
| Show SwiftUI inspector | `⌘` + click on a view |

---

## 🧠 The eight worth memorising first

If you learn nothing else from this page:

| | |
|---|---|
| `⇧⌘O` | Open Quickly — replaces most navigating |
| `⌃⌘J` | Jump to definition |
| `⌃⌘←` | Go back where you were |
| `⌘⇧F` | Find across the project |
| `⌘R` / `⌘.` | Run / stop |
| `⌘U` | Test |
| `⌘\` | Breakpoint |
| `⌘/` | Comment |

---

<sub>Part of **[suryakulshreshtha/SuryaKulshreshtha](https://github.com/suryakulshreshtha/SuryaKulshreshtha)** — see the repository index for the current test-automation work.</sub>
