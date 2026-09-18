WIREFRAME_SYSTEM_PROMPT = """Generate a low-fidelity desktop UX wireframe. Black and white, flat orthographic interface, no gradients, no shadows, no decorative illustration. Use clear rectangular placeholders, strong hierarchy, consistent spacing, visible section boundaries, and realistic landing-page composition. Do not render a polished UI."""

def wireframe_prompt(user_prompt): return WIREFRAME_SYSTEM_PROMPT+"\n\nProduct brief:\n"+user_prompt

def ui_prompt(user_prompt): return "Render a polished production-quality web UI from the supplied wireframe. Preserve composition, section order, placement, whitespace and proportions. Add typography, color, cards, charts, icons and styling without changing the layout skeleton.\nProduct brief:\n"+user_prompt
