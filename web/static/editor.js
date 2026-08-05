// 编辑器小工具：让 textarea 支持 Tab 缩进 / Shift+Tab 反缩进 / 多行选区整体缩进
(function () {
  const TAB = "    "; // 4 个空格（Python 社区习惯）

  function indentSelection(textarea, delta) {
    const value = textarea.value;
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const lineStart = value.lastIndexOf("\n", start - 1) + 1;

    if (start === end) {
      // 无选区：光标处插入，或把当前行反缩进
      if (delta > 0) {
        textarea.value = value.slice(0, start) + TAB + value.slice(end);
        textarea.selectionStart = textarea.selectionEnd = start + TAB.length;
      } else {
        if (value.slice(lineStart, lineStart + TAB.length) === TAB) {
          textarea.value = value.slice(0, lineStart) + value.slice(lineStart + TAB.length);
          textarea.selectionStart = textarea.selectionEnd = Math.max(lineStart, start - TAB.length);
        }
      }
    } else {
      // 多行选区：对每一行统一缩进/反缩进
      const lines = value.slice(lineStart, end).split("\n");
      const out = lines
        .map((l) => (delta > 0 ? TAB + l : l.startsWith(TAB) ? l.slice(TAB.length) : l))
        .join("\n");
      textarea.value = value.slice(0, lineStart) + out + value.slice(end);
      textarea.selectionStart = lineStart;
      textarea.selectionEnd = lineStart + out.length;
    }
  }

  function enableTabIndent(textarea) {
    textarea.addEventListener("keydown", function (e) {
      if (e.key === "Tab") {
        e.preventDefault();
        indentSelection(this, e.shiftKey ? -1 : 1);
      }
    });
  }

  document.querySelectorAll("textarea").forEach(enableTabIndent);
})();
