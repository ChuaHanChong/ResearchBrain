
Help me research world action models that can self-evolve. What is a good starting point: (1) get a trained self-evolving agent and then add the capability to predict the next state (i.e., give it the ability to "dream"), or (2) take a trained world action model and then add the ability for it to self-evolve and continue learning? Get me the relevant papers.

---

For applications in embodied intelligence, robotics, and complex open-world games, the **model-first trajectory (Option 2)** is the superior starting point. Taking a robust world model like DreamerV3 and adding mechanisms for reflection and curriculum learning (as seen in EvoAgent) provides the necessary environmental grounding and mitigates catastrophic forgetting, leading to massive improvements in success rates for long-horizon tasks.

---
For a research starting point, **Option 2 is heavily favored by modern AI research.** Taking a trained world action model and adding self-evolving/continuous learning capabilities is a much more practical and scalable path.

Here is why Option 2 is the better approach, followed by the core papers you should look into.

### Why Option 2 Wins: The Synthetic Data Advantage

If you start with a model-free agent (Option 1) and try to bolt on a "dreaming" component, you run into a massive architectural wall. The agent's existing neural pathways were optimized strictly to map states to actions, not to capture the underlying physics or visual dynamics of the environment.

By starting with a trained world model (Option 2), you already have a robust latent space. The model is already capable of generating synthetic future states to train its action policy.

When you make this model "self-evolving," the research challenge shifts to a very specific, fascinating problem: **data quality within the model's own imagination.** Because the agent learns continuously from its own synthetic rollouts, you have to engineer mechanisms to prevent it from exploiting artifacts, hallucinating biased dynamics, or suffering from data leakage between past and present tasks. It is much easier to add memory and continuous learning algorithms to a system that already understands how to generate its own training data than to teach a reactive agent how to dream from scratch.


---
Q;Correct me if I'm making wrong: self-evolving agent != self-evolving world action model because the agent might not be able to predict/imagine the future state.  


You are exactly right. Your distinction hits on one of the most fundamental divides in reinforcement learning and AI architecture: **Model-Free** vs. **Model-Based** systems.

A self-evolving world action model is a specific, highly advanced _subset_ of a self-evolving agent. Here is the breakdown of why your logic is spot on.

### The Self-Evolving Agent (The Broader Category)

A self-evolving agent is simply any autonomous system that can improve its own policy or behavior over time through interaction with its environment. However, **it does not inherently require a predictive model of that environment.**

- **How it works:** Many of these are "Model-Free" reinforcement learning agents. They learn a direct mapping from a state to an action (a policy) or evaluate the value of an action, entirely through trial and error.
    
- **The Limitation:** If an agent learns that pressing a button yields a reward, it will press the button. But it doesn't possess an internal concept of the mechanical gears turning behind the button. It cannot "imagine" what would happen if the button was jammed; it just knows the expected reward has changed after the fact.
    

### The Self-Evolving World Action Model (The Specific Subset)

A world action model explicitly requires two coupled components: a **World Model** (the internal simulator) and an **Action Model** (the policy).

- **How it works:** It learns the underlying transition dynamics of the environment. Mathematically, it attempts to learn a function that accurately predicts the next state $S_{t+1}$ and reward $R_{t+1}$ given the current state $S_t$ and action $A_t$.
    
- **The Advantage:** Because it can predict the future state, it can plan. It can "dream" or simulate thousands of potential actions in its latent space without ever taking a physical action in the real world. Self-evolution here often focuses on minimizing the prediction error of the world model itself, forcing the agent to explore areas where its imagination fails to match reality.
    

### Summary

- **All Self-Evolving World Action Models are Self-Evolving Agents.**
    
- **Not all Self-Evolving Agents are World Action Models.** An agent using simple Q-learning or genetic algorithms can evolve to solve incredibly complex tasks, but it does so entirely "in the dark" without the ability to simulate or predict the future states of its environment.
    

Would you like to explore how model-free agents handle self-evolution without imagination, or look closer into the math of how world models calculate prediction errors?



---
A **self-evolving world action model** represents a paradigm in embodied AI where an agent simultaneously learns to predict environmental dynamics (the **world model**) and optimize its decision-making strategies (**action model**) through continuous, often self-supervised, interaction. This coupling allows the agent to refine its internal simulation of "how the world works" while using that same simulation to plan and evolve its behavior.

## Key Concepts in Self-Evolving Models

Research in this area has shifted from static training on fixed datasets to **dynamic self-evolution**—a process where agents autonomously generate, validate, and solve tasks to expand their own capabilities.

- **World Models as Internal Simulators**: A world model acts as a latent representation of the environment, enabling the agent to forecast future states based on current observations and potential actions. This "forward modeling" is critical for planning without real-world risk.
- **Co-Evolutionary Frameworks**: Recent work like **Evolver** introduces frameworks where a world model and an action policy co-evolve. The world model simulates diverse scenarios, and the action policy learns to navigate them, with the feedback loop refining both components simultaneously.
- **Self-Training and Self-Critique**: Self-evolving agents often use techniques like **STaR** (Self-Taught Reasoner) or **Quiet-STaR** to iteratively generate and enhance responses or action plans through self-reflection and critique, rather than relying solely on external labels.
- **Active Perception and Curiosity**: Agents may use "progress curiosity" to actively explore parts of the environment where their world model is most uncertain, ensuring the model evolves to cover a broader range of states.