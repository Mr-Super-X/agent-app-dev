import { defineConfig } from 'vitepress'
import { withMermaid } from 'vitepress-plugin-mermaid'

export default withMermaid(
  defineConfig({
  title: '大模型 Agent 应用开发学习教程',
  description: '从初级开发者到生产级 Agent 工程师的体系化教程',
  lang: 'zh-CN',
  // GitHub Pages 子路径部署必须设 base，否则 asset/CSS 加载 404
  base: '/agent-app-dev/',
  // 排除 superpowers 工作目录(spec/plan)与未发布草稿
  srcExclude: ['**/superpowers/**'],
  // examples 路由 TODO: v1.1 用 rewrites 真正生效，v1.0 临时关掉
  ignoreDeadLinks: true,
  themeConfig: {
    nav: [
      { text: '入门教程', link: '/getting-started/00-roadmap' },
      { text: '生产进阶', link: '/production/00-prerequisites' },
      { text: '考试中心', link: '/exam/AI-Agent-Engineer-Exam' }
    ],
    sidebar: {
      '/operations/': [
        { text: '部署文档（DEPLOY）', link: 'operations/deploy' },
        { text: 'E2E 跑通记录', link: 'operations/e2e-run' }
      ],
      '/examples/': [
        { text: '00 hello-llm', link: 'https://github.com/Mr-Super-X/agent-app-dev/tree/main/examples/00-hello-llm' },
        { text: '01 prompt-cot', link: 'https://github.com/Mr-Super-X/agent-app-dev/tree/main/examples/01-prompt-cot' },
        { text: '02 rag-pipeline', link: 'https://github.com/Mr-Super-X/agent-app-dev/tree/main/examples/02-rag-pipeline' },
        { text: '03 tool-calling', link: 'https://github.com/Mr-Super-X/agent-app-dev/tree/main/examples/03-tool-calling' },
        { text: '04 agent-architecture', link: 'https://github.com/Mr-Super-X/agent-app-dev/tree/main/examples/04-agent-architecture' },
        { text: '05 frameworks-compare', link: 'https://github.com/Mr-Super-X/agent-app-dev/tree/main/examples/05-frameworks-compare' },
        { text: '06 customer-service', link: 'https://github.com/Mr-Super-X/agent-app-dev/tree/main/examples/06-customer-service' },
        { text: '07 code-generation', link: 'https://github.com/Mr-Super-X/agent-app-dev/tree/main/examples/07-code-generation' },
        { text: '08 multi-agent', link: 'https://github.com/Mr-Super-X/agent-app-dev/tree/main/examples/08-multi-agent' },
        { text: '09 system-design', link: 'https://github.com/Mr-Super-X/agent-app-dev/tree/main/examples/09-system-design' },
        { text: '10 evaluation', link: 'https://github.com/Mr-Super-X/agent-app-dev/tree/main/examples/10-evaluation' },
        { text: '11 security', link: 'https://github.com/Mr-Super-X/agent-app-dev/tree/main/examples/11-security' },
        { text: '12 engineering-async', link: 'https://github.com/Mr-Super-X/agent-app-dev/tree/main/examples/12-engineering-async' }
      ],
      '/getting-started/': [
        {
          text: '阶段 1·打地基',
          items: [
            { text: '00 三阶段总览', link: '/getting-started/00-roadmap' },
            { text: '01 基础认知', link: '/getting-started/01-basics/01-llm-and-agent' },
            { text: '02 LLM 基础', link: '/getting-started/01-basics/02-llm-fundamentals' }
          ]
        },
        {
          text: '阶段 2·核心能力',
          items: [
            { text: '03 提示工程', link: '/getting-started/02-core/03-prompt-engineering' },
            { text: '04 RAG', link: '/getting-started/02-core/04-rag' },
            { text: '05 工具调用', link: '/getting-started/02-core/05-tool-calling' },
            { text: '06 Agent 架构', link: '/getting-started/02-core/06-agent-architecture' }
          ]
        },
        {
          text: '阶段 3·实战与视野',
          items: [
            { text: '07 Agent 框架', link: '/getting-started/03-advanced/07-frameworks' },
            { text: '08 场景题', link: '/getting-started/03-advanced/08-scenarios' },
            { text: '09 开放问题', link: '/getting-started/03-advanced/09-open-questions' }
          ]
        }
      ],
      '/production/': [
        { text: '前置与读者起点', link: '/production/00-prerequisites' },
        { text: 'Ch1 系统设计', link: '/production/01-system-design' },
        { text: 'Ch2 评估与优化', link: '/production/02-evaluation' },
        { text: 'Ch3 安全与风险', link: '/production/03-security' },
        { text: 'Ch4 工程实战', link: '/production/04-engineering' }
      ],
      '/exam/': [
        { text: 'AI Agent 工程师 P5 笔试卷', link: '/exam/AI-Agent-Engineer-Exam' }
      ]
    },
    search: { provider: 'local' },
    outline: { level: [2, 3] }
  }
  })
)

