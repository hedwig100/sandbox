import { readFileSync } from "node:fs";
import { join } from "node:path";
import postcss from "postcss";
import { describe, expect, it } from "vitest";

describe("panel scrolling layout", () => {
  it("constrains both panels and gives their content independent scroll areas", () => {
    const root = postcss.parse(readFileSync(join(process.cwd(), "src/app/globals.css"), "utf8"));
    const declarations = (selector: string) => {
      const result = new Map<string, string>();
      root.walkRules(selector, (rule) => rule.walkDecls((declaration) => {
        result.set(declaration.prop, declaration.value);
      }));
      return result;
    };

    expect(declarations(".appShell").get("grid-template-rows")).toContain("minmax(0,1fr)");
    expect(declarations(".chatPanel").get("min-height")).toBe("0");
    expect(declarations(".chatPanel").get("overflow")).toBe("hidden");
    expect(declarations(".conversation").get("min-height")).toBe("0");
    expect(declarations(".conversation").get("overflow-y")).toBe("auto");
    expect(declarations(".board").get("min-height")).toBe("0");
    expect(declarations(".board").get("overflow")).toBe("hidden");
    expect(declarations(".boardScroll").get("flex")).toBe("1");
    expect(declarations(".boardScroll").get("min-height")).toBe("0");
    expect(declarations(".boardScroll").get("overflow-y")).toBe("auto");
  });
});
