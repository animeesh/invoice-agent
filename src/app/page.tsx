"use client";

import { Tool } from "@/components/tool";
import { CatchAllActionRenderProps, useCopilotAction } from "@copilotkit/react-core";
import { CopilotKitCSSProperties, CopilotSidebar } from "@copilotkit/react-ui";
import { useState } from "react";

export default function CopilotKitPage() {
  const [themeColor] = useState("#1216d3");

  return (
    <main style={{ "--copilot-kit-primary-color": themeColor } as CopilotKitCSSProperties}>
      <YourMainContent themeColor={themeColor} />
      <CopilotSidebar
        clickOutsideToClose={false}
        defaultOpen={true}
        labels={{
          title: "Invoice Assistant",
          initial: "👋 Hi there! I'm your Invoice Assistant powered by Agno. I can help you Track Invoice status, Extract invoice details, and provide Invoice drafting.\n\nTry asking me about:\n- **Invoice Status**: \"What's the status of invoice #123?\"\n- **Invoice Details**: \"Show me the details for invoice #456\"\n- **Invoice Drafting**: \"Help me draft a new invoice\"\n\nI'll use real-time financial data to provide you with comprehensive investment analysis!"
        }}
      />
    </main>
  );
}

function YourMainContent({ themeColor }: { themeColor: string }) {
  useCopilotAction({
    name: "*",
    render: (props: CatchAllActionRenderProps) => <Tool {...props} themeColor={themeColor} />,
  });

  return (
    <div
      style={{ backgroundColor: themeColor }}
      className="h-screen w-screen flex justify-center items-center flex-col transition-colors duration-300"
    >
      <div className="bg-white/20 backdrop-blur-md p-8 rounded-2xl shadow-xl max-w-2xl w-full">
      
        <h1 className="text-4xl font-bold text-white mb-2 text-center"> Allianz - CopilotKit x Agno</h1>
        <p className="text-gray-200 text-center italic">Invoice assistant journey starts here 🚀</p>
      </div>
    </div>
  );
}
