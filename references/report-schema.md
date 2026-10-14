# Printable Report Schema

The renderer accepts UTF-8 JSON. Unknown fields are ignored; missing optional fields render as empty sections.

```json
{
  "meta": {
    "title": "错题诊断与变式训练",
    "student": "小宇",
    "grade": "三年级",
    "date": "2026-10-14",
    "topic": "两位数减法退位"
  },
  "summary": "会列式，但退位后没有把1个十换成10个一。",
  "original": {
    "question": "52 - 28 = ?",
    "student_answer": "34",
    "correct_answer": "24",
    "first_divergence": "从个位计算开始：2不够减8时进行了退位，但个位只算成12-8，十位仍按5-2计算。"
  },
  "diagnosis": [
    {
      "label": "退位后的位值更新",
      "confidence": "中",
      "evidence": "个位使用了12-8，但十位没有从5变为4。",
      "alternative": "也可能是书写时漏改十位，需要用一道对比题确认。"
    }
  ],
  "child_explanation": "向十位借来的1，不是消失了，而是换成了10个一；同时十位要少1。",
  "worked_example": [
    "看个位：2不够减8。",
    "从5个十中拿1个十，换成10个一，所以个位变成12。",
    "十位剩4，个位12-8=4，十位4-2=2，答案是24。"
  ],
  "practice": [
    {
      "title": "第一关 · 同类巩固",
      "subtitle": "先把退位动作做完整",
      "questions": ["61 - 27 =", "73 - 48 ="]
    },
    {
      "title": "第二关 · 对比判断",
      "subtitle": "先判断要不要退位，再计算",
      "questions": ["64 - 21 =", "64 - 29 ="]
    },
    {
      "title": "第三关 · 迁移挑战",
      "subtitle": "换一种问法，方法仍然一样",
      "questions": ["停车场有82辆车，开走37辆，还剩多少辆？", "□ - 26 = 38，□里填多少？"]
    }
  ],
  "review": [
    {"when": "明天", "questions": ["72 - 46 =", "80 - 35 ="]},
    {"when": "3—7天后", "questions": ["91 - 57 =", "一本书有74页，已经看了38页，还剩多少页？"]}
  ],
  "answers": ["34", "25", "43", "35", "45辆", "64", "26", "45", "34", "36页"],
  "adult_note": "下次重点观察：退位后，孩子是否会主动把十位数字减1。先保证准确，再计时。"
}
```

Keep `answers` in the same order as all practice questions followed by all review questions.

