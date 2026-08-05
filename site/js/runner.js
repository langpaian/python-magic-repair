// 主线程侧的执行器：管理 Pyodide Worker，带超时与"卡住重启"。
// 学习者写死循环时，worker 会卡住 → 主线程超时 → 杀掉重建。
const Runner = (() => {
  let worker = null;
  let readyPromise = null;
  let msgId = 0;
  const pending = {};

  function spawn() {
    worker = new Worker("js/worker.js");
    worker.onmessage = (e) => {
      const p = pending[e.data.id];
      if (p) {
        clearTimeout(p.timer);
        delete pending[e.data.id];
        p.resolve(e.data);
      }
    };
    worker.onerror = () => {
      // worker 崩了：杀掉，让下一次调用重建
      if (worker) worker.terminate();
      worker = null;
      readyPromise = null;
      for (const k of Object.keys(pending)) {
        clearTimeout(pending[k].timer);
        pending[k].resolve({ ok: false, stderr: "（机器摔了一跤……请再试一次。）" });
        delete pending[k];
      }
    };
  }

  function post(type, payload, timeout, stuckMsg) {
    return new Promise((resolve) => {
      if (!worker) spawn();
      const id = "m" + (++msgId);
      const timer = setTimeout(() => {
        if (worker) worker.terminate();
        worker = null;
        readyPromise = null;
        delete pending[id];
        resolve({ ok: false, timeout: true, stderr: stuckMsg });
      }, timeout);
      pending[id] = { resolve, timer };
      worker.postMessage({ id, type, ...payload });
    });
  }

  function init() {
    if (readyPromise) return readyPromise;
    readyPromise = new Promise((resolve, reject) => {
      if (!worker) spawn();
      const id = "init-" + (++msgId);
      const timer = setTimeout(() => {
        delete pending[id];
        reject(new Error("机器醒得太慢"));
      }, 90000);
      pending[id] = {
        resolve: (m) => {
          if (m.type === "ready") { clearTimeout(timer); resolve(); }
          else { clearTimeout(timer); reject(new Error("init failed")); }
        },
        timer,
      };
      worker.postMessage({ id, type: "init" });
    });
    readyPromise.catch(() => { readyPromise = null; });
    return readyPromise;
  }

  async function run(code) {
    await init();
    return post("run", { code }, 5000, "（机器卡住了……是不是有个死循环在兜圈子？）");
  }

  async function judge(code, tests) {
    await init();
    return post("judge", { code, tests }, 12000, "（机器等太久了……它是不是在死循环里打转？）");
  }

  return { init, run, judge };
})();
