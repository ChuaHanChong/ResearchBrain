# Reading list — non-arxiv resources (blogs, repos, docs); commented out, not scraped by run.py.

# --- RL for LLMs ---
# https://cameronrwolfe.substack.com/p/online-rl  # Online versus Offline RL for LLMs
# https://cameronrwolfe.substack.com/p/grpo-tricks  # GRPO++: Tricks for Making RL Actually Work
# https://huggingface.co/posts/Kseniase/304021452230579  # 10 Latest Preference Optimization Techniques
# https://accessible-dragon-75f.notion.site/RL-Grokking-Recipe-How-Can-We-Enable-LLMs-to-Solve-Previously-Unsolvable-Tasks-with-RL-100a1714e6778062bae5eafad8e7677d  # RL Grokking Recipe: How Can We Enable LLMs to Solve Previously Unsolvable Tasks with RL?
# https://relieved-cafe-fe1.notion.site/JustRL-Scaling-a-1-5B-LLM-with-a-Simple-RL-Recipe-24f6198b0b6b80e48e74f519bfdaf0a8  # JustRL: Scaling a 1.5B LLM with a Simple RL Recipe
# https://github.com/google-deepmind/disco_rl

# --- LLM evaluation (LLM-as-Judge) ---
# https://eugeneyan.com/writing/eval-process/  # An LLM-as-Judge Won't Save The Product—Fixing Your Process Will
# https://eugeneyan.com/writing/llm-evaluators/  # Evaluating the Effectiveness of LLM-Evaluators (aka LLM-as-Judge)

# --- Fine-tuning & distillation ---
# https://thinkingmachines.ai/blog/lora/  # LoRA Without Regret
# https://huggingface.co/spaces/HuggingFaceH4/on-policy-distillation
# https://yumoxu.notion.site/multi-teacher-on-policy-distillation

# --- Transformers & LLM architecture ---
# https://goyalpramod.github.io/blogs/Transformers_laid_out/  # Transformers Laid Out
# https://alexzhang13.github.io/blog/2025/rlm/  # Recursive Language Models

# --- Agents ---
# https://tencentcloudadp.github.io/youtu-agent/
# https://github.com/Memento-Teams/Memento-Skills
# https://github.com/nousresearch/hermes-agent

# --- Multimodal & vision (repos) ---
# https://github.com/EvolvingLMMs-Lab/lmms-engine  # A simple, unified multimodal models training engine. Lean, flexible, and built for hacking at scale.
# https://github.com/alexstoken/image-matching-models

# --- Embodied, robotics & spatial intelligence ---
# https://drfeifei.substack.com/p/from-words-to-worlds-spatial-intelligence  # From Words to Worlds: Spatial Intelligence is AI’s Next Frontier
# https://github.com/huggingface/lerobot
# https://genesis-world.readthedocs.io/en/latest/

papers = [
    "https://arxiv.org/abs/1312.5602",  # Playing Atari with Deep Reinforcement Learning
    "https://arxiv.org/abs/1507.08750",  # Action-Conditional Video Prediction using Deep Networks in Atari Games
    "https://arxiv.org/abs/1612.00796",  # Overcoming catastrophic forgetting in neural networks
    "https://arxiv.org/abs/1612.03144",  # Feature Pyramid Networks for Object Detection
    "https://arxiv.org/abs/1705.05363",  # Curiosity-driven Exploration by Self-supervised Prediction
    "https://arxiv.org/abs/1706.04261",  # The 'something something' video database for learning and evaluating visual common sense
    "https://arxiv.org/abs/1707.05300",  # Reverse Curriculum Generation for Reinforcement Learning
    "https://arxiv.org/abs/1707.06347",  # Proximal Policy Optimization Algorithms
    "https://arxiv.org/abs/1801.01290",  # Soft Actor-Critic: Off-Policy Maximum Entropy Deep Reinforcement Learning with a Stochastic Actor
    "https://arxiv.org/abs/1801.03924",  # The Unreasonable Effectiveness of Deep Features as a Perceptual Metric
    "https://arxiv.org/abs/1803.01529",  # LSTD: A Low-Shot Transfer Detector for Object Detection
    "https://arxiv.org/abs/1803.01534",  # Path Aggregation Network for Instance Segmentation
    "https://arxiv.org/abs/1803.05407",  # Averaging Weights Leads to Wider Optima and Better Generalization
    "https://arxiv.org/abs/1803.10122",  # World Models
    "https://arxiv.org/abs/1804.02748",  # Scaling Egocentric Vision: The EPIC-KITCHENS Dataset
    "https://arxiv.org/abs/1805.07914",  # Imitating Latent Policies from Observation
    "https://arxiv.org/abs/1806.04728",  # RepMet: Representative-based metric learning for classification and one-shot object detection
    "https://arxiv.org/abs/1806.09655",  # Learning what you can do before doing anything
    "https://arxiv.org/abs/1806.10293",  # QT-Opt: Scalable Deep Reinforcement Learning for Vision-Based Robotic Manipulation
    "https://arxiv.org/abs/1810.07121",  # Multiple Interactions Made Easy (MIME): Large Scale Demonstrations Data for Imitation
    "https://arxiv.org/abs/1810.09091",  # SG-One: Similarity Guidance Network for One-Shot Semantic Segmentation
    "https://arxiv.org/abs/1810.12894",  # Exploration by Random Network Distillation
    "https://arxiv.org/abs/1811.04551",  # Learning Latent Dynamics for Planning from Pixels
    "https://arxiv.org/abs/1811.11507",  # One-Shot Instance Segmentation
    "https://arxiv.org/abs/1812.01717",  # Towards Accurate Generative Models of Video: A New Metric & Challenges
    "https://arxiv.org/abs/1812.03399",  # Efficient transfer learning and online adaptation with latent variable models for continuous control
    "https://arxiv.org/abs/1812.06162",  # An Empirical Model of Large-Batch Training
    "https://arxiv.org/abs/1901.01753",  # Paired Open-Ended Trailblazer (POET): Endlessly Generating Increasingly Complex and Diverse Learning Environments and Their Solutions
    "https://arxiv.org/abs/1901.09184",  # Action Robust Reinforcement Learning and Applications in Continuous Control
    "https://arxiv.org/abs/1903.00374",  # Model-Based Reinforcement Learning for Atari
    "https://arxiv.org/abs/1903.04128",  # Manipulation by Feel: Touch-Based Control with Deep Predictive Models
    "https://arxiv.org/abs/1903.10654",  # Failure-Scenario Maker for Rule-Based Agent using Multi-agent Adversarial Reinforcement Learning and its Application to Autonomous Driving
    "https://arxiv.org/abs/1906.03327",  # HowTo100M: Learning a Text-Video Embedding by Watching Hundred Million Narrated Video Clips
    "https://arxiv.org/abs/1906.08253",  # When to Trust Your Model: Model-Based Policy Optimization
    "https://arxiv.org/abs/1906.08880",  # Variable Impedance Control in End-Effector Space: An Action Space for Reinforcement Learning in Contact-Rich Tasks
    "https://arxiv.org/abs/1907.06987",  # A Short Note on the Kinetics-700 Human Action Dataset
    "https://arxiv.org/abs/1908.01998",  # Few-Shot Object Detection with Attention-RPN and Multi-Relation Detector
    "https://arxiv.org/abs/1909.04915",  # Data-efficient Model Learning and Prediction for Contact-rich Manipulation Tasks
    "https://arxiv.org/abs/1909.12271",  # RLBench: The Robot Learning Benchmark & Learning Environment
    "https://arxiv.org/abs/1909.13032",  # Meta R-CNN : Towards General Solver for Instance-level Few-shot Learning
    "https://arxiv.org/abs/1910.10897",  # Meta-World: A Benchmark and Evaluation for Multi-Task and Meta Reinforcement Learning
    "https://arxiv.org/abs/1910.11215",  # RoboNet: Large-Scale Multi-Robot Learning
    "https://arxiv.org/abs/1910.11956",  # Relay Policy Learning: Solving Long-Horizon Tasks via Imitation and Reinforcement Learning
    "https://arxiv.org/abs/1911.04052",  # Scaling Robot Supervision to Hundreds of Hours with RoboTurk: Robotic Manipulation Dataset through Human Reasoning and Dexterity
    "https://arxiv.org/abs/1911.10601",  # Scaling active inference
    "https://arxiv.org/abs/1911.12529",  # One-Shot Object Detection with Co-Attention and Co-Excitation
    "https://arxiv.org/abs/1912.01603",  # Dream to Control: Learning Behaviors by Latent Imagination
    "https://arxiv.org/abs/1912.06321",  # Sim2Real Predictivity: Does Evaluation in Simulation Predict Real-World Performance?
    "https://arxiv.org/abs/2001.03070",  # Benchmarking In-Hand Manipulation
    "https://arxiv.org/abs/2002.04741",  # Progressive Object Transfer Detection
    "https://arxiv.org/abs/2002.07421",  # EHSOD: CAM-Guided End-to-end Hybrid-Supervised Object Detection with Cascade Refinement
    "https://arxiv.org/abs/2002.07953",  # Universal Domain Adaptation through Self Supervision
    "https://arxiv.org/abs/2003.01239",  # Rapidly Adaptable Legged Robots via Evolutionary Meta-Learning
    "https://arxiv.org/abs/2003.06800",  # OS2D: One-Stage One-Shot Object Detection by Matching Anchor Features
    "https://arxiv.org/abs/2003.08515",  # SAPIEN: A SimulAted Part-based Interactive ENvironment
    "https://arxiv.org/abs/2004.02684",  # Attribute Mix: Semantic Data Augmentation for Fine Grained Recognition
    "https://arxiv.org/abs/2004.02857",  # Beyond the Nav-Graph: Vision-and-Language Navigation in Continuous Environments
    "https://arxiv.org/abs/2005.05960",  # Planning to Explore via Self-Supervised World Models
    "https://arxiv.org/abs/2005.13239",  # MOPO: Model-based Offline Policy Optimization
    "https://arxiv.org/abs/2006.00626",  # In the Eye of the Beholder: Gaze and Actions in First Person Video
    "https://arxiv.org/abs/2007.04309",  # Self-Supervised Policy Adaptation during Deployment
    "https://arxiv.org/abs/2007.07853",  # Active World Model Learning with Progress Curiosity
    "https://arxiv.org/abs/2007.07986",  # Boosting Weakly Supervised Object Detection with Progressive Knowledge Transfer
    "https://arxiv.org/abs/2008.01655",  # Deep Visual Odometry with Adaptive Memory
    "https://arxiv.org/abs/2009.06732",  # Efficient Transformers: A Survey
    "https://arxiv.org/abs/2009.12293",  # robosuite: A Modular Simulation Framework and Benchmark for Robot Learning
    "https://arxiv.org/abs/2010.02193",  # Mastering Atari with Discrete World Models
    "https://arxiv.org/abs/2010.07954",  # Room-Across-Room: Multilingual Vision-and-Language Navigation with Dense Spatiotemporal Grounding
    "https://arxiv.org/abs/2010.11929",  # An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale
    "https://arxiv.org/abs/2010.11944",  # Accelerating Reinforcement Learning with Learned Skill Priors
    "https://arxiv.org/abs/2010.13303",  # Trajectory-wise Multiple Choice Learning for Dynamics Generalization in Reinforcement Learning
    "https://arxiv.org/abs/2010.15920",  # Recovery RL: Safe Reinforcement Learning with Learned Recovery Zones
    "https://arxiv.org/abs/2011.01968",  # Learning 3D Dynamic Scene Representations for Robot Manipulation
    "https://arxiv.org/abs/2011.07215",  # SoftGym: Benchmarking Deep Reinforcement Learning for Deformable Object Manipulation
    "https://arxiv.org/abs/2011.11270",  # COCOI: Contact-aware Online Context Inference for Generalizable Non-planar Pushing
    "https://arxiv.org/abs/2012.03912",  # MultiON: Benchmarking Semantic Map Memory using Multi-Object Navigation
    "https://arxiv.org/abs/2012.04293",  # CRAFT: A Benchmark for Causal Reasoning About Forces and inTeractions
    "https://arxiv.org/abs/2012.06644",  # Regularizing Action Policies for Smooth Control with Reinforcement Learning
    "https://arxiv.org/abs/2012.12556",  # A Survey on Visual Transformer
    "https://arxiv.org/abs/2101.01169",  # Transformers in Vision: A Survey
    "https://arxiv.org/abs/2101.05181",  # Memory-Augmented Reinforcement Learning for Image-Goal Navigation
    "https://arxiv.org/abs/2101.12195",  # Playable Video Generation
    "https://arxiv.org/abs/2102.06746",  # The Importance of Being a Band: Finite-Sample Exact Distribution-Free Prediction Sets for Functional Data
    "https://arxiv.org/abs/2102.06810",  # Understanding self-supervised Learning Dynamics without Contrastive Pairs
    "https://arxiv.org/abs/2103.00020",  # Learning Transferable Visual Models From Natural Language Supervision
    "https://arxiv.org/abs/2103.04918",  # A Survey of Embodied AI: From Simulators to Research Tasks
    "https://arxiv.org/abs/2103.10369",  # Combining Pessimism with Optimism for Robust and Efficient Model-Based Deep Reinforcement Learning
    "https://arxiv.org/abs/2103.14256",  # Learning Reactive and Predictive Differentiable Controllers for Switching Linear Dynamical Models
    "https://arxiv.org/abs/2103.15358",  # Multi-Scale Vision Longformer: A New Vision Transformer for High-Resolution Image Encoding
    "https://arxiv.org/abs/2103.16397",  # 3D AffordanceNet: A Benchmark for Visual Object Affordance Understanding
    "https://arxiv.org/abs/2104.02057",  # An Empirical Study of Training Self-Supervised Vision Transformers
    "https://arxiv.org/abs/2104.02646",  # gradSim: Differentiable simulation for system identification and visuomotor control
    "https://arxiv.org/abs/2104.03311",  # PlasticineLab: A Soft-Body Manipulation Benchmark with Differentiable Physics
    "https://arxiv.org/abs/2104.03344",  # OVANet: One-vs-All Network for Universal Domain Adaptation
    "https://arxiv.org/abs/2104.03602",  # SiT: Self-supervised vIsion Transformer
    "https://arxiv.org/abs/2104.08212",  # MT-Opt: Continuous Multi-Task Robotic Reinforcement Learning at Scale
    "https://arxiv.org/abs/2104.10218",  # Episodic Memory Model for Learning Robotic Manipulation Tasks
    "https://arxiv.org/abs/2104.11181",  # H2O: Two Hands Manipulating Objects for First Person Interaction Recognition
    "https://arxiv.org/abs/2104.11203",  # Reset-Free Reinforcement Learning via Multi-Task Learning: Learning Dexterous Manipulation Behaviors without Human Intervention
    "https://arxiv.org/abs/2104.11213",  # ManipulaTHOR: A Framework for Visual Object Manipulation
    "https://arxiv.org/abs/2104.11227",  # Multiscale Vision Transformers
    "https://arxiv.org/abs/2104.12763",  # MDETR -- Modulated Detection for End-to-End Multi-Modal Understanding
    "https://arxiv.org/abs/2104.13921",  # Open-vocabulary Object Detection via Vision and Language Knowledge Distillation
    "https://arxiv.org/abs/2104.14294",  # Emerging Properties in Self-Supervised Vision Transformers
    "https://arxiv.org/abs/2104.14984",  # CAT: Cross-Attention Transformer for One-Shot Object Detection
    "https://arxiv.org/abs/2105.04553",  # Self-Supervised Learning with Swin Transformers
    "https://arxiv.org/abs/2105.04906",  # VICReg: Variance-Invariance-Covariance Regularization for Self-Supervised Learning
    "https://arxiv.org/abs/2105.10919",  # Continual World: A Robotic Benchmark For Continual Reinforcement Learning
    "https://arxiv.org/abs/2105.13677",  # ResT: An Efficient Transformer for Visual Recognition
    "https://arxiv.org/abs/2106.03911",  # XIRL: Cross-embodiment Inverse Reinforcement Learning
    "https://arxiv.org/abs/2106.05526",  # Simplifying Deep Reinforcement Learning via Self-Supervision
    "https://arxiv.org/abs/2106.08254",  # BEiT: BERT Pre-Training of Image Transformers
    "https://arxiv.org/abs/2106.08261",  # Physion: Evaluating Physical Prediction from Vision in Humans and Machines
    "https://arxiv.org/abs/2106.08796",  # Tactile Sim-to-Real Policy Transfer via Real-to-Sim Image Translation
    "https://arxiv.org/abs/2106.09785",  # Efficient Self-supervised Vision Transformers for Representation Learning
    "https://arxiv.org/abs/2107.00641",  # Focal Self-attention for Local-Global Interactions in Vision Transformers
    "https://arxiv.org/abs/2107.02239",  # Vision Xformers: Efficient Attention for Image Classification
    "https://arxiv.org/abs/2107.03996",  # Learning Vision-Guided Quadrupedal Locomotion End-to-End with Cross-Modal Transformers
    "https://arxiv.org/abs/2107.04034",  # RMA: Rapid Motor Adaptation for Legged Robots
    "https://arxiv.org/abs/2107.06263",  # CMT: Convolutional Neural Networks Meet Vision Transformers
    "https://arxiv.org/abs/2107.14483",  # ManiSkill: Generalizable Manipulation Skill Benchmark with Large-Scale Demonstrations
    "https://arxiv.org/abs/2108.03298",  # What Matters in Learning from Offline Human Demonstrations for Robot Manipulation
    "https://arxiv.org/abs/2108.05988",  # TVT: Transferable Vision Transformer for Unsupervised Domain Adaptation
    "https://arxiv.org/abs/2109.00137",  # Implicit Behavioral Cloning
    "https://arxiv.org/abs/2109.01134",  # Learning to Prompt for Vision-Language Models
    "https://arxiv.org/abs/2109.04027",  # Taxim: An Example-based Simulation Model for GelSight Tactile Sensors
    "https://arxiv.org/abs/2109.06165",  # CDTrans: Cross-domain Transformer for Unsupervised Domain Adaptation
    "https://arxiv.org/abs/2109.08203",  # Torch.manual_seed(3407) is all you need: On the influence of random seeds in deep learning architectures for computer vision
    "https://arxiv.org/abs/2109.08238",  # Habitat-Matterport 3D Dataset (HM3D): 1000 Large-scale 3D Environments for Embodied AI
    "https://arxiv.org/abs/2109.13202",  # MiniHack the Planet: A Sandbox for Open-Ended Reinforcement Learning Research
    "https://arxiv.org/abs/2109.13396",  # Bridge Data: Boosting Generalization of Robotic Skills with Cross-Domain Datasets
    "https://arxiv.org/abs/2110.01411",  # Deep Reinforcement Learning Versus Evolution Strategies: A Comparative Survey
    "https://arxiv.org/abs/2110.03374",  # Model Adaptation: Historical Contrastive Learning for Unsupervised Domain Adaptation without Source Data
    "https://arxiv.org/abs/2110.07058",  # Ego4D: Around the World in 3,000 Hours of Egocentric Video
    "https://arxiv.org/abs/2110.09408",  # HRFormer: High-Resolution Transformer for Dense Prediction
    "https://arxiv.org/abs/2111.00765",  # Validate on Sim, Detect on Real -- Model Selection for Domain Randomization
    "https://arxiv.org/abs/2111.01236",  # Multi-Scale High-Resolution Vision Transformer for Semantic Segmentation
    "https://arxiv.org/abs/2111.03930",  # Tip-Adapter: Training-free CLIP-Adapter for Better Vision-Language Modeling
    "https://arxiv.org/abs/2111.06091",  # A Survey of Visual Transformers
    "https://arxiv.org/abs/2111.06377",  # Masked Autoencoders Are Scalable Vision Learners
    "https://arxiv.org/abs/2111.07991",  # LiT: Zero-Shot Transfer with Locked-image text Tuning
    "https://arxiv.org/abs/2111.09793",  # Unsupervised Online Learning for Robotic Interestingness with Visual Memory
    "https://arxiv.org/abs/2111.09883",  # Swin Transformer V2: Scaling Up Capacity and Resolution
    "https://arxiv.org/abs/2111.09886",  # SimMIM: A Simple Framework for Masked Image Modeling
    "https://arxiv.org/abs/2111.10050",  # Combined Scaling for Zero-shot Transfer Learning
    "https://arxiv.org/abs/2111.12941",  # Exploiting Both Domain-specific and Invariant Knowledge via a Win-win Transformer for Unsupervised Domain Adaptation
    "https://arxiv.org/abs/2112.01506",  # Sample Complexity of Robust Reinforcement Learning with a Generative Model
    "https://arxiv.org/abs/2112.01526",  # MViTv2: Improved Multiscale Vision Transformers for Classification and Detection
    "https://arxiv.org/abs/2112.02814",  # A Survey of Deep Learning for Low-Shot Object Detection
    "https://arxiv.org/abs/2112.03227",  # CALVIN: A Benchmark for Language-Conditioned Policy Learning for Long-Horizon Robot Manipulation Tasks
    "https://arxiv.org/abs/2112.03857",  # Grounded Language-Image Pre-training
    "https://arxiv.org/abs/2112.06442",  # Contact-Rich Manipulation of a Flexible Object based on Deep Predictive Learning using Vision and Tactility
    "https://arxiv.org/abs/2112.09106",  # RegionCLIP: Region-based Language-Image Pretraining
    "https://arxiv.org/abs/2112.11010",  # MPViT: Multi-Path Vision Transformer for Dense Prediction
    "https://arxiv.org/abs/2112.15402",  # Relational Experience Replay: Continual Learning by Adaptively Tuning Task-wise Relationship
    "https://arxiv.org/abs/2201.02373",  # Mirror Learning: A Unifying Framework of Policy Optimisation
    "https://arxiv.org/abs/2201.02605",  # Detecting Twenty-thousand Classes using Image-level Supervision
    "https://arxiv.org/abs/2201.02609",  # Generalized Category Discovery
    "https://arxiv.org/abs/2201.03871",  # Combining Learning-based Locomotion Policy with Model-based Manipulation for Legged Mobile Manipulators
    "https://arxiv.org/abs/2201.07207",  # Language Models as Zero-Shot Planners: Extracting Actionable Knowledge for Embodied Agents
    "https://arxiv.org/abs/2201.08355",  # Sim-to-Lab-to-Real: Safe Reinforcement Learning with Shielding and Generalization Guarantees
    "https://arxiv.org/abs/2201.12086",  # BLIP: Bootstrapping Language-Image Pre-training for Unified Vision-Language Understanding and Generation
    "https://arxiv.org/abs/2201.13248",  # SafeAPT: Safe Simulation-to-Real Robot Learning using Diverse Policies Learned in Simulation
    "https://arxiv.org/abs/2202.02005",  # BC-Z: Zero-Shot Task Generalization with Robotic Imitation Learning
    "https://arxiv.org/abs/2202.09834",  # Real-time Model Predictive Control and System Identification Using Differentiable Physics Simulation
    "https://arxiv.org/abs/2203.01577",  # HOI4D: A 4D Egocentric Dataset for Category-Level Human-Object Interaction
    "https://arxiv.org/abs/2203.01914",  # Playable Environments: Video Manipulation in Space and Time
    "https://arxiv.org/abs/2203.03485",  # Self-directed Learning of Action Models using Exploratory Planning
    "https://arxiv.org/abs/2203.05557",  # Conditional Prompt Learning for Vision-Language Models
    "https://arxiv.org/abs/2203.06856",  # ACID: Action-Conditional Implicit Visual Dynamics for Deformable Object Manipulation
    "https://arxiv.org/abs/2203.07669",  # Progressive End-to-End Object Detection in Crowded Scenes
    "https://arxiv.org/abs/2203.09093",  # Semantic-aligned Fusion Transformer for One-shot Object Detection
    "https://arxiv.org/abs/2203.11926",  # Focal Modulation Networks
    "https://arxiv.org/abs/2203.11931",  # MetaMorph: Learning Universal Controllers with Transformers
    "https://arxiv.org/abs/2203.12555",  # GriTS: Grid table similarity metric for table structure recognition
    "https://arxiv.org/abs/2203.13116",  # Egocentric Prediction of Action Target in 3D
    "https://arxiv.org/abs/2203.14465",  # STaR: Bootstrapping Reasoning With Reasoning
    "https://arxiv.org/abs/2203.14712",  # Assembly101: A Large-Scale Multi-View Video Dataset for Understanding Procedural Activities
    "https://arxiv.org/abs/2203.15709",  # OakInk: A Large-scale Knowledge Repository for Understanding Hand-Object Interaction
    "https://arxiv.org/abs/2203.16265",  # SeqTR: A Simple yet Universal Network for Visual Grounding
    "https://arxiv.org/abs/2203.16513",  # PromptDet: Towards Open-vocabulary Detection using Uncurated Images
    "https://arxiv.org/abs/2203.16527",  # Exploring Plain Vision Transformer Backbones for Object Detection
    "https://arxiv.org/abs/2203.17273",  # FindIt: Generalized Localization with Natural Language Queries
    "https://arxiv.org/abs/2204.00598",  # Socratic Models: Composing Zero-Shot Multimodal Reasoning with Language
    "https://arxiv.org/abs/2204.01697",  # MaxViT: Multi-Axis Vision Transformer
    "https://arxiv.org/abs/2204.02041",  # Automating Reinforcement Learning with Example-based Resets
    "https://arxiv.org/abs/2204.03139",  # DiffCloud: Real-to-Sim from Point Clouds with Differentiable Simulation and Rendering of Deformable Objects
    "https://arxiv.org/abs/2204.07683",  # Safe Self-Refinement for Transformer-based Domain Adaptation
    "https://arxiv.org/abs/2204.12581",  # RAMBO-RL: Robust Adversarial Model-Based Offline Reinforcement Learning
    "https://arxiv.org/abs/2204.13662",  # ARCTIC: A Dataset for Dexterous Bimanual Hand-Object Manipulation
    "https://arxiv.org/abs/2205.00363",  # Visual Spatial Reasoning
    "https://arxiv.org/abs/2205.01917",  # CoCa: Contrastive Captioners are Image-Text Foundation Models
    "https://arxiv.org/abs/2205.06230",  # Simple Open-Vocabulary Object Detection with Vision Transformers
    "https://arxiv.org/abs/2205.06311",  # Provably Safe Deep Reinforcement Learning for Robotic Manipulation in Human Environments
    "https://arxiv.org/abs/2205.08534",  # Vision Transformer Adapter for Dense Predictions
    "https://arxiv.org/abs/2205.09329",  # Dataset Pruning: Reducing Training Data by Examining Generalization Influence
    "https://arxiv.org/abs/2205.09991",  # Planning with Diffusion for Flexible Behavior Synthesis
    "https://arxiv.org/abs/2205.10268",  # B-cos Networks: Alignment is All We Need for Interpretability
    "https://arxiv.org/abs/2205.14756",  # EfficientViT: Multi-Scale Linear Attention for High-Resolution Dense Prediction
    "https://arxiv.org/abs/2205.14949",  # HiViT: Hierarchical Vision Transformer Meets Masked Image Modeling
    "https://arxiv.org/abs/2206.00238",  # Transferable Reward Learning by Dynamics-Agnostic Discriminator Ensemble
    "https://arxiv.org/abs/2206.02072",  # Deciding What to Model: Value-Equivalent Sampling for Reinforcement Learning
    "https://arxiv.org/abs/2206.02647",  # Scaling Vision Transformers to Gigapixel Images via Hierarchical Self-Supervised Learning
    "https://arxiv.org/abs/2206.05165",  # Multifidelity Reinforcement Learning with Control Variates
    "https://arxiv.org/abs/2206.05836",  # GLIPv2: Unifying Localization and Vision-Language Understanding
    "https://arxiv.org/abs/2206.07643",  # Coarse-to-Fine Vision-Language Pre-training with Fusion in the Backbone
    "https://arxiv.org/abs/2206.08522",  # VLMbench: A Compositional Benchmark for Vision-and-Language Manipulation
    "https://arxiv.org/abs/2206.09682",  # SafeBench: A Benchmarking Platform for Safety Evaluation of Autonomous Vehicles
    "https://arxiv.org/abs/2206.14176",  # DayDreamer: World Models for Physical Robot Learning
    "https://arxiv.org/abs/2206.14244",  # Masked World Models for Visual Control
    "https://arxiv.org/abs/2207.01887",  # Open-Vocabulary Multi-Label Classification via Multi-Modal Knowledge Transfer
    "https://arxiv.org/abs/2207.07560",  # Skill-based Model-based Reinforcement Learning
    "https://arxiv.org/abs/2207.10821",  # Rethinking Sim2Real: Lower Fidelity Simulation Leads to Higher Sim2Real Transfer in Navigation
    "https://arxiv.org/abs/2207.12380",  # Task-Relevant Failure Detection for Trajectory Predictors in Autonomous Vehicles
    "https://arxiv.org/abs/2207.13050",  # Efficient High-Resolution Deep Learning: A Survey
    "https://arxiv.org/abs/2207.13438",  # A Contact-Safe Reinforcement Learning Framework for Contact-Rich Robot Manipulation
    "https://arxiv.org/abs/2209.05451",  # Perceiver-Actor: A Multi-Task Transformer for Robotic Manipulation
    "https://arxiv.org/abs/2209.07753",  # Code as Policies: Language Model Programs for Embodied Control
    "https://arxiv.org/abs/2209.09407",  # DetCLIP: Dictionary-Enriched Visual-Concept Paralleled Pre-training for Open-world Detection
    "https://arxiv.org/abs/2209.10021",  # DiffTune: Auto-Tuning through Auto-Differentiation
    "https://arxiv.org/abs/2209.13052",  # Training Efficient Controllers via Analytic Policy Gradient
    "https://arxiv.org/abs/2209.15639",  # F-VLM: Open-Vocabulary Object Detection upon Frozen Vision and Language Models
    "https://arxiv.org/abs/2210.02697",  # DexGraspNet: A Large-Scale Robotic Dexterous Grasp Dataset for General Objects Based on Simulation
    "https://arxiv.org/abs/2210.03087",  # Iterative Vision-and-Language Navigation
    "https://arxiv.org/abs/2210.03094",  # VIMA: General Robot Manipulation with Multimodal Prompts
    "https://arxiv.org/abs/2210.03629",  # ReAct: Synergizing Reasoning and Acting in Language Models
    "https://arxiv.org/abs/2210.04887",  # In-Hand Object Rotation via Rapid Motor Adaptation
    "https://arxiv.org/abs/2210.05639",  # Discovered Policy Optimisation
    "https://arxiv.org/abs/2210.05714",  # Visual Language Maps for Robot Navigation
    "https://arxiv.org/abs/2210.06407",  # Interactive Language: Talking to Robots in Real Time
    "https://arxiv.org/abs/2210.10765",  # When to Ask for Help: Proactive Interventions in Autonomous Reinforcement Learning
    "https://arxiv.org/abs/2210.12320",  # Online Adaptive Policy Selection in Time-Varying Systems: No-Regret via Contractive Perturbations
    "https://arxiv.org/abs/2210.13066",  # DaXBench: Benchmarking Deformable Object Manipulation with Differentiable Physics
    "https://arxiv.org/abs/2210.13702",  # DeXtreme: Transfer of Agile In-hand Manipulation from Simulation to Reality
    "https://arxiv.org/abs/2210.17067",  # Unified Optimal Transport Framework for Universal Domain Adaptation
    "https://arxiv.org/abs/2211.03876",  # CoNMix for Source-free Single and Multi-target Domain Adaptation
    "https://arxiv.org/abs/2211.09699",  # PromptCap: Prompt-Guided Task-Aware Image Captioning
    "https://arxiv.org/abs/2211.10277",  # Task Residual for Tuning Vision-Language Models
    "https://arxiv.org/abs/2211.10435",  # PAL: Program-aided Language Models
    "https://arxiv.org/abs/2211.10831",  # Joint Embedding Predictive Architectures Focus on Slow Features
    "https://arxiv.org/abs/2211.11559",  # Visual Programming: Compositional visual reasoning without training
    "https://arxiv.org/abs/2211.12588",  # Program of Thoughts Prompting: Disentangling Computation from Reasoning for Numerical Reasoning Tasks
    "https://arxiv.org/abs/2211.14680",  # A Physics-informed Diffusion Model for High-fidelity Flow Field Reconstruction
    "https://arxiv.org/abs/2211.15944",  # The Effectiveness of World Models for Continual Reinforcement Learning
    "https://arxiv.org/abs/2212.03194",  # DiffTune$^+$: Hyperparameter-Free Auto-Tuning using Auto-Differentiation
    "https://arxiv.org/abs/2212.06817",  # RT-1: Robotics Transformer for Real-World Control at Scale
    "https://arxiv.org/abs/2212.07143",  # Reproducible scaling laws for contrastive language-image learning
    "https://arxiv.org/abs/2212.07740",  # Sim-to-Real Transfer for Quadrupedal Locomotion via Terrain Transformer
    "https://arxiv.org/abs/2212.08013",  # FlexiViT: One Model for All Patch Sizes
    "https://arxiv.org/abs/2212.08333",  # AnyGrasp: Robust and Efficient Grasp Perception in Spatial and Temporal Domains
    "https://arxiv.org/abs/2212.14020",  # A System-Level View on Out-of-Distribution Data in Robotics
    "https://arxiv.org/abs/2301.02419",  # Exploring Efficient Few-shot Adaptation for Vision Transformers
    "https://arxiv.org/abs/2301.04104",  # Mastering Diverse Domains through World Models
    "https://arxiv.org/abs/2301.05226",  # See, Think, Confirm: Interactive Prompting Between Vision and Language Models for Knowledge-based Visual Reasoning
    "https://arxiv.org/abs/2301.08028",  # A Tutorial on Meta-Reinforcement Learning
    "https://arxiv.org/abs/2301.08243",  # Self-Supervised Learning from Images with a Joint-Embedding Predictive Architecture
    "https://arxiv.org/abs/2301.10602",  # DreamWaQ: Learning Robust Quadrupedal Locomotion With Implicit Terrain Imagination via Deep Reinforcement Learning
    "https://arxiv.org/abs/2301.11915",  # Understanding Self-Supervised Pretraining with Part-Aware Representation Learning
    "https://arxiv.org/abs/2301.11972",  # Using Social Cues to Recognize Task Failures for HRI: Overview, State-of-the-Art, and Future Directions
    "https://arxiv.org/abs/2301.13261",  # Emergence of Maps in the Memories of Blind Navigation Agents
    "https://arxiv.org/abs/2302.00111",  # Learning Universal Policies via Text-Guided Video Generation
    "https://arxiv.org/abs/2302.00674",  # Improving Few-Shot Generalization by Exploring and Exploiting Auxiliary Data
    "https://arxiv.org/abs/2302.00923",  # Multimodal Chain-of-Thought Reasoning in Language Models
    "https://arxiv.org/abs/2302.01107",  # A Survey on Efficient Training of Transformers
    "https://arxiv.org/abs/2302.01877",  # AdaptDiffuser: Diffusion Models as Adaptive Self-evolving Planners
    "https://arxiv.org/abs/2302.04659",  # ManiSkill2: A Unified Benchmark for Generalizable Manipulation Skills
    "https://arxiv.org/abs/2302.05209",  # A Survey on Causal Reinforcement Learning
    "https://arxiv.org/abs/2302.05442",  # Scaling Vision Transformers to 22 Billion Parameters
    "https://arxiv.org/abs/2302.05543",  # Adding Conditional Control to Text-to-Image Diffusion Models
    "https://arxiv.org/abs/2302.08242",  # Tuning computer vision models with task rewards
    "https://arxiv.org/abs/2302.14045",  # Language Is Not All You Need: Aligning Perception with Language Models
    "https://arxiv.org/abs/2303.01906",  # Generalized Semantic Segmentation by Self-Supervised Source Domain Projection and Multi-Level Contrastive Learning
    "https://arxiv.org/abs/2303.04137",  # Diffusion Policy: Visuomotor Policy Learning via Action Diffusion
    "https://arxiv.org/abs/2303.04671",  # Visual ChatGPT: Talking, Drawing and Editing with Visual Foundation Models
    "https://arxiv.org/abs/2303.05499",  # Grounding DINO: Marrying DINO with Grounded Pre-Training for Open-Set Object Detection
    "https://arxiv.org/abs/2303.05512",  # PAC-NeRF: Physics Augmented Continuum Neural Radiance Fields for Geometry-Agnostic System Identification
    "https://arxiv.org/abs/2303.07110",  # Upcycling Models under Domain and Category Shift
    "https://arxiv.org/abs/2303.07280",  # Vision-Language Models as Success Detectors
    "https://arxiv.org/abs/2303.08128",  # ViperGPT: Visual Inference via Python Execution for Reasoning
    "https://arxiv.org/abs/2303.11331",  # EVA-02: A Visual Representation for Neon Genesis
    "https://arxiv.org/abs/2303.11381",  # MM-REACT: Prompting ChatGPT for Multimodal Reasoning and Action
    "https://arxiv.org/abs/2303.13076",  # CORA: Adapting CLIP for Open-Vocabulary Detection with Region Prompting and Anchor Pre-Matching
    "https://arxiv.org/abs/2303.13434",  # Patch-Mix Transformer for Unsupervised Domain Adaptation: A Game Perspective
    "https://arxiv.org/abs/2303.14240",  # Adaptive Base-class Suppression and Prior Guidance Network for One-Shot Object Detection
    "https://arxiv.org/abs/2304.03223",  # DexDeform: Dexterous Deformable Object Manipulation with Human Demonstrations and Differentiable Physics
    "https://arxiv.org/abs/2304.03977",  # EMP-SSL: Towards Self-Supervised Learning in One Training Epoch
    "https://arxiv.org/abs/2304.04321",  # ARNOLD: A Benchmark for Language-Grounded Task Learning With Continuous States in Realistic 3D Scenes
    "https://arxiv.org/abs/2304.04514",  # DetCLIPv2: Scalable Open-Vocabulary Object Detection Pre-training via Word-Region Alignment
    "https://arxiv.org/abs/2304.06250",  # RSIR Transformer: Hierarchical Vision Transformer using Random Sampling Windows and Important Region Windows
    "https://arxiv.org/abs/2304.06712",  # What does CLIP know about a red circle? Visual prompt engineering for VLMs
    "https://arxiv.org/abs/2304.07193",  # DINOv2: Learning Robust Visual Features without Supervision
    "https://arxiv.org/abs/2304.13705",  # Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware
    "https://arxiv.org/abs/2304.14369",  # Learning Neural Constitutive Laws From Motion Observations for Generalizable PDE Dynamics
    "https://arxiv.org/abs/2305.00104",  # MMViT: Multiscale Multiview Vision Transformers
    "https://arxiv.org/abs/2305.00976",  # TMR: Text-to-Motion Retrieval Using Contrastive 3D Human Motion Synthesis
    "https://arxiv.org/abs/2305.04866",  # Causal Policy Gradient for Whole-Body Mobile Manipulation
    "https://arxiv.org/abs/2305.05665",  # ImageBind: One Embedding Space To Bind Them All
    "https://arxiv.org/abs/2305.06341",  # Non-Euclidean Motion Planning with Graphs of Geodesically-Convex Sets
    "https://arxiv.org/abs/2305.06500",  # InstructBLIP: Towards General-purpose Vision-Language Models with Instruction Tuning
    "https://arxiv.org/abs/2305.07011",  # Region-Aware Pretraining for Open-Vocabulary Object Detection with Vision Transformers
    "https://arxiv.org/abs/2305.09880",  # A survey of the Vision Transformers and their CNN-Transformer based Variants
    "https://arxiv.org/abs/2305.12821",  # FurnitureBench: Reproducible Real-World Benchmark for Long-Horizon Complex Manipulation
    "https://arxiv.org/abs/2305.13301",  # Training Diffusion Models with Reinforcement Learning
    "https://arxiv.org/abs/2305.13622",  # Continual Learning with Strong Experience Replay
    "https://arxiv.org/abs/2305.13689",  # Know Your Self-supervised Learning: A Survey on Image-based Generative and Discriminative Training
    "https://arxiv.org/abs/2305.13840",  # Control-A-Video: Controllable Text-to-Video Diffusion Models with Motion Prior and Reward Feedback Learning
    "https://arxiv.org/abs/2305.14654",  # Barkour: Benchmarking Animal-level Agility with Quadruped Robots
    "https://arxiv.org/abs/2305.14676",  # GRILL: Grounded Vision-language Pre-training via Aligning Text and Image Regions
    "https://arxiv.org/abs/2305.14992",  # Reasoning with Language Model is Planning with World Model
    "https://arxiv.org/abs/2305.17110",  # IndustReal: Transferring Contact-Rich Assembly Tasks from Simulation to Reality
    "https://arxiv.org/abs/2305.17216",  # Generating Images with Multimodal Language Models
    "https://arxiv.org/abs/2305.17250",  # Self-Supervised Reinforcement Learning that Transfers using Random Features
    "https://arxiv.org/abs/2305.18035",  # Physics-Informed Computer Vision: A Review and Perspectives
    "https://arxiv.org/abs/2305.18712",  # Can We Evaluate Domain Adaptation Models Without Target-Domain Labels?
    "https://arxiv.org/abs/2306.01708",  # TIES-Merging: Resolving Interference When Merging Models
    "https://arxiv.org/abs/2306.02018",  # VideoComposer: Compositional Video Synthesis with Motion Controllability
    "https://arxiv.org/abs/2306.02572",  # Introduction to Latent Variable Energy-Based Models: A Path Towards Autonomous Machine Intelligence
    "https://arxiv.org/abs/2306.03310",  # LIBERO: Benchmarking Knowledge Transfer for Lifelong Robot Learning
    "https://arxiv.org/abs/2306.03514",  # Recognize Anything: A Strong Image Tagging Model
    "https://arxiv.org/abs/2306.05353",  # Negotiated Reasoning: On Provably Addressing Relative Over-Generalization
    "https://arxiv.org/abs/2306.06189",  # FasterViT: Fast Vision Transformers with Hierarchical Attention
    "https://arxiv.org/abs/2306.06799",  # On the Efficacy of 3D Point Cloud Reinforcement Learning
    "https://arxiv.org/abs/2306.08543",  # MiniLLM: Knowledge Distillation of Large Language Models
    "https://arxiv.org/abs/2306.09344",  # DreamSim: Learning New Dimensions of Human Visual Similarity using Synthetic Data
    "https://arxiv.org/abs/2306.09459",  # Recurrent Action Transformer with Memory
    "https://arxiv.org/abs/2306.09683",  # Scaling Open-Vocabulary Object Detection
    "https://arxiv.org/abs/2306.10007",  # Robot Learning with Sensorimotor Pre-training
    "https://arxiv.org/abs/2306.11565",  # HomeRobot: Open-Vocabulary Mobile Manipulation
    "https://arxiv.org/abs/2306.13394",  # MME: A Comprehensive Evaluation Benchmark for Multimodal Large Language Models
    "https://arxiv.org/abs/2306.13549",  # A Survey on Multimodal Large Language Models
    "https://arxiv.org/abs/2306.13643",  # LightGlue: Local Feature Matching at Light Speed
    "https://arxiv.org/abs/2306.14824",  # Kosmos-2: Grounding Multimodal Large Language Models to the World
    "https://arxiv.org/abs/2306.15195",  # Shikra: Unleashing Multimodal LLM's Referential Dialogue Magic
    "https://arxiv.org/abs/2306.15668",  # Physion++: Evaluating Physical Scene Understanding that Requires Online Inference of Different Physical Properties
    "https://arxiv.org/abs/2306.15724",  # REFLECT: Summarizing Robot Experiences for Failure Explanation and Correction
    "https://arxiv.org/abs/2306.15880",  # Towards Open Vocabulary Learning: A Survey
    "https://arxiv.org/abs/2307.00595",  # RH20T: A Comprehensive Robotic Dataset for Learning Diverse Skills in One-Shot
    "https://arxiv.org/abs/2307.01452",  # Causal Reinforcement Learning: A Survey
    "https://arxiv.org/abs/2307.03601",  # GPT4RoI: Instruction Tuning Large Language Model on Region-of-Interest
    "https://arxiv.org/abs/2307.04054",  # Deep Unsupervised Learning Using Spike-Timing-Dependent Plasticity
    "https://arxiv.org/abs/2307.05933",  # BiRP: Learning Robot Generalized Bimanual Coordination using Relative Parameterization Method on Human Demonstration
    "https://arxiv.org/abs/2307.05973",  # VoxPoser: Composable 3D Value Maps for Robotic Manipulation with Language Models
    "https://arxiv.org/abs/2307.06281",  # MMBench: Is Your Multi-modal Model an All-around Player?
    "https://arxiv.org/abs/2307.06304",  # Patch n' Pack: NaViT, a Vision Transformer for any Aspect Ratio and Resolution
    "https://arxiv.org/abs/2307.06423",  # Bi-Touch: Bimanual Tactile Manipulation with Sim-to-Real Deep Reinforcement Learning
    "https://arxiv.org/abs/2307.08927",  # Multi-Stage Cable Routing through Hierarchical Imitation Learning
    "https://arxiv.org/abs/2307.09120",  # Light-Weight Vision Transformer with Parallel Local and Global Self-Attention
    "https://arxiv.org/abs/2307.09220",  # A Survey on Open-Vocabulary Detection and Segmentation: Past, Present, and Future
    "https://arxiv.org/abs/2307.09955",  # XSkill: Cross Embodiment Skill Discovery
    "https://arxiv.org/abs/2307.10224",  # RL-ViGen: A Reinforcement Learning Benchmark for Visual Generalization
    "https://arxiv.org/abs/2307.12698",  # MC-JEPA: A Joint-Embedding Predictive Architecture for Self-Supervised Learning of Motion and Content Features
    "https://arxiv.org/abs/2307.12813",  # Described Object Detection: Liberating Object Detection with Flexible Expressions
    "https://arxiv.org/abs/2307.12983",  # Parallel $Q$-Learning: Scaling Off-policy Reinforcement Learning under Massively Parallel Simulation
    "https://arxiv.org/abs/2307.15818",  # RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control
    "https://arxiv.org/abs/2308.00692",  # LISA: Reasoning Segmentation via Large Language Model
    "https://arxiv.org/abs/2308.01399",  # Learning to Model the World with Language
    "https://arxiv.org/abs/2308.05602",  # Object Goal Navigation with Recursive Implicit Maps
    "https://arxiv.org/abs/2308.05659",  # AD-CLIP: Adapting Domains in Prompt Space Using CLIP
    "https://arxiv.org/abs/2308.07498",  # DREAMWALKER: Mental Planning for Continuous Vision-Language Navigation
    "https://arxiv.org/abs/2308.08089",  # DragNUWA: Fine-grained Control in Video Generation by Integrating Text, Image, and Trajectory
    "https://arxiv.org/abs/2308.09713",  # Dynamic 3D Gaussians: Tracking by Persistent Dynamic View Synthesis
    "https://arxiv.org/abs/2308.10677",  # Visual Crowd Analysis: Open Research Problems
    "https://arxiv.org/abs/2308.12216",  # SG-Former: Self-guided Transformer with Evolving Token Reallocation
    "https://arxiv.org/abs/2308.12952",  # BridgeData V2: A Dataset for Robot Learning at Scale
    "https://arxiv.org/abs/2308.14636",  # Towards Standardized Disturbance Rejection Testing of Legged Robot Locomotion with Linear Impactor: A Preliminary Study, Observations, and Implications
    "https://arxiv.org/abs/2309.01909",  # A Survey on Physics Informed Reinforcement Learning: Review and Open Problems
    "https://arxiv.org/abs/2309.02031",  # A survey on efficient vision transformers: algorithms, techniques, and performance benchmarking
    "https://arxiv.org/abs/2309.05519",  # NExT-GPT: Any-to-Any Multimodal LLM
    "https://arxiv.org/abs/2309.05858",  # Uncovering mesa-optimization algorithms in Transformers
    "https://arxiv.org/abs/2309.07906",  # Generative Image Dynamics
    "https://arxiv.org/abs/2309.08603",  # Closing the Loop on Runtime Monitors with Fallback-Safe MPC
    "https://arxiv.org/abs/2309.08912",  # Delving into Multimodal Prompting for Fine-grained Visual Classification
    "https://arxiv.org/abs/2309.09979",  # General In-Hand Object Rotation with Vision and Touch
    "https://arxiv.org/abs/2309.11069",  # Dynamic Tiling: A Model-Agnostic, Adaptive, Scalable, and Inference-Data-Centric Approach for Efficient and Accurate Small Object Detection
    "https://arxiv.org/abs/2309.13037",  # GELLO: A General, Low-Cost, and Intuitive Teleoperation Framework for Robot Manipulators
    "https://arxiv.org/abs/2309.13475",  # Detecting and Mitigating System-Level Anomalies of Vision-Based Controllers
    "https://arxiv.org/abs/2309.14322",  # Small-scale proxies for large-scale Transformer training instabilities
    "https://arxiv.org/abs/2309.15129",  # Evaluating Cognitive Maps and Planning in Large Language Models with CogEval
    "https://arxiv.org/abs/2309.15278",  # Out of Sight, Still in Mind: Reasoning and Planning about Unobserved Objects with Video Tracking Enabled Memory Models
    "https://arxiv.org/abs/2309.16014",  # Graph-level Representation Learning with Joint-Embedding Predictive Architectures
    "https://arxiv.org/abs/2309.16797",  # Promptbreeder: Self-Referential Self-Improvement Via Prompt Evolution
    "https://arxiv.org/abs/2309.17024",  # HoloAssist: an Egocentric Human Interaction Dataset for Interactive AI Assistants in the Real World
    "https://arxiv.org/abs/2309.17080",  # GAIA-1: A Generative World Model for Autonomous Driving
    "https://arxiv.org/abs/2309.17400",  # Directly Fine-Tuning Diffusion Models on Differentiable Rewards
    "https://arxiv.org/abs/2309.17444",  # LLM-grounded Video Diffusion Models
    "https://arxiv.org/abs/2310.00433",  # Active-Perceptive Motion Generation for Mobile Manipulation
    "https://arxiv.org/abs/2310.00632",  # Win-Win: Training High-Resolution Vision Transformers from Two Windows
    "https://arxiv.org/abs/2310.00754",  # Analyzing and Mitigating Object Hallucination in Large Vision-Language Models
    "https://arxiv.org/abs/2310.02239",  # MiniGPT-5: Interleaved Vision-and-Language Generation via Generative Vokens
    "https://arxiv.org/abs/2310.03744",  # Improved Baselines with Visual Instruction Tuning
    "https://arxiv.org/abs/2310.04406",  # Language Agent Tree Search Unifies Reasoning Acting and Planning in Language Models
    "https://arxiv.org/abs/2310.05916",  # Interpreting CLIP's Image Representation via Text-Based Decomposition
    "https://arxiv.org/abs/2310.05922",  # FLATTEN: optical FLow-guided ATTENtion for consistent text-to-video editing
    "https://arxiv.org/abs/2310.06114",  # Learning Interactive Real-World Simulators
    "https://arxiv.org/abs/2310.06253",  # A Unified View on Solving Objective Mismatch in Model-Based Reinforcement Learning
    "https://arxiv.org/abs/2310.08367",  # MCU: An Evaluation Framework for Open-Ended Game Agents
    "https://arxiv.org/abs/2310.08465",  # MotionDirector: Motion Customization of Text-to-Video Diffusion Models
    "https://arxiv.org/abs/2310.08576",  # Learning to Act from Actionless Videos through Dense Correspondences
    "https://arxiv.org/abs/2310.08864",  # Open X-Embodiment: Robotic Learning Datasets and RT-X Models
    "https://arxiv.org/abs/2310.09053",  # DATT: Deep Adaptive Trajectory Tracking for Quadrotor Control
    "https://arxiv.org/abs/2310.10625",  # Video Language Planning
    "https://arxiv.org/abs/2310.11441",  # Set-of-Mark Prompting Unleashes Extraordinary Visual Grounding in GPT-4V
    "https://arxiv.org/abs/2310.12567",  # Safety-Gymnasium: A Unified Safe Reinforcement Learning Benchmark
    "https://arxiv.org/abs/2310.15308",  # SAM-CLIP: Merging Vision Foundation Models towards Semantic and Spatial Understanding
    "https://arxiv.org/abs/2310.17552",  # Model-Based Runtime Monitoring with Interactive Imitation Learning
    "https://arxiv.org/abs/2310.17596",  # MimicGen: A Data Generation System for Scalable Robot Learning using Human Demonstrations
    "https://arxiv.org/abs/2310.18969",  # Analyzing Vision Transformers for Image Classification in Class Embedding Space
    "https://arxiv.org/abs/2311.00530",  # Advances in Embodied Navigation Using Large Language Models: A Survey
    "https://arxiv.org/abs/2311.01378",  # Vision-Language Foundation Models as Effective Robot Imitators
    "https://arxiv.org/abs/2311.03099",  # Language Models are Super Mario: Absorbing Abilities from Homologous Models as a Free Lunch
    "https://arxiv.org/abs/2311.03351",  # Uni-O4: Unifying Online and Offline Deep Reinforcement Learning with Multi-Step On-Policy Optimization
    "https://arxiv.org/abs/2311.04157",  # A Simple Interpretable Transformer for Fine-Grained Image Classification and Analysis
    "https://arxiv.org/abs/2311.05437",  # LLaVA-Plus: Learning to Use Tools for Creating Multimodal Agents
    "https://arxiv.org/abs/2311.07499",  # Bridging the Sim-to-Real Gap with Dynamic Compliance Tuning for Industrial Insertion
    "https://arxiv.org/abs/2311.09191",  # Domain Aligned CLIP for Few-shot Classification
    "https://arxiv.org/abs/2311.10111",  # VideoCon: Robust Video-Language Alignment via Contrast Captions
    "https://arxiv.org/abs/2311.11893",  # Towards Proactive Safe Human-Robot Collaborations via Data-Efficient Conditional Behavior Prediction
    "https://arxiv.org/abs/2311.12198",  # PhysGaussian: Physics-Integrated 3D Gaussians for Generative Dynamics
    "https://arxiv.org/abs/2311.12244",  # Provable Representation with Efficient Planning for Partial Observable Reinforcement Learning
    "https://arxiv.org/abs/2311.12424",  # Looped Transformers are Better at Learning Learning Algorithms
    "https://arxiv.org/abs/2311.12631",  # GPT4Motion: Scripting Physical Motions in Text-to-Video Generation via Blender-Oriented GPT Planning
    "https://arxiv.org/abs/2311.13099",  # PIE-NeRF: Physics-based Interactive Elastodynamics with NeRF
    "https://arxiv.org/abs/2311.13601",  # Visual In-Context Prompting
    "https://arxiv.org/abs/2311.15153",  # Predicting Gradient is Better: Exploring Self-Supervised Learning for SAR ATR with a Joint-Embedding Predictive Architecture
    "https://arxiv.org/abs/2311.16502",  # MMMU: A Massive Multi-discipline Multimodal Understanding and Reasoning Benchmark for Expert AGI
    "https://arxiv.org/abs/2311.17117",  # Animate Anyone: Consistent and Controllable Image-to-Video Synthesis for Character Animation
    "https://arxiv.org/abs/2311.18259",  # Ego-Exo4D: Understanding Skilled Human Activity from First- and Third-Person Perspectives
    "https://arxiv.org/abs/2312.00583",  # DeformGS: Scene Flow in Highly Deformable Scenes for Deformable Object Manipulation
    "https://arxiv.org/abs/2312.00845",  # VMC: Video Motion Customization using Temporal Attention Adaption for Text-to-Video Diffusion Models
    "https://arxiv.org/abs/2312.01990",  # SARA-RT: Scaling up Robotics Transformers with Self-Adaptive Robust Attention
    "https://arxiv.org/abs/2312.03641",  # MotionCtrl: A Unified and Flexible Motion Controller for Video Generation
    "https://arxiv.org/abs/2312.03673",  # On the Role of the Action Space in Robot Manipulation Learning and Sim-to-Real Transfer
    "https://arxiv.org/abs/2312.04000",  # LiDAR: Sensing Linear Probing Performance in Joint Embedding SSL Architectures
    "https://arxiv.org/abs/2312.04684",  # LaRS: Latent Reasoning Skills for Chain-of-Thought Reasoning
    "https://arxiv.org/abs/2312.06709",  # AM-RADIO: Agglomerative Vision Foundation Model -- Reduce All Domains Into One
    "https://arxiv.org/abs/2312.07871",  # MLNet: Mutual Learning Network with Neighborhood Invariance for Universal Domain Adaptation
    "https://arxiv.org/abs/2312.08762",  # Multi-modal Latent Space Learning for Chain-of-Thought Reasoning in Language Models
    "https://arxiv.org/abs/2312.10439",  # Simple Image-level Classification Improves Open-vocabulary Object Detection
    "https://arxiv.org/abs/2312.10812",  # Learning to Act without Actions
    "https://arxiv.org/abs/2312.11460",  # Hybrid Internal Model: Learning Agile Legged Locomotion with Simulated Robot Response
    "https://arxiv.org/abs/2312.12148",  # Parameter-Efficient Fine-Tuning Methods for Pretrained Language Models: A Critical Review and Assessment
    "https://arxiv.org/abs/2312.13139",  # Unleashing Large-Scale Video Generative Pre-training for Visual Robot Manipulation
    "https://arxiv.org/abs/2312.13286",  # Generative Multimodal Models are In-Context Learners
    "https://arxiv.org/abs/2312.14135",  # V*: Guided Visual Search as a Core Mechanism in Multimodal LLMs
    "https://arxiv.org/abs/2312.17681",  # FlowVid: Taming Imperfect Optical Flows for Consistent Video-to-Video Synthesis
    "https://arxiv.org/abs/2312.17686",  # Multiscale Vision Transformers meet Bipartite Matching for efficient single-stage Action Localization
    "https://arxiv.org/abs/2401.02117",  # Mobile ALOHA: Learning Bimanual Mobile Manipulation with Low-Cost Whole-Body Teleoperation
    "https://arxiv.org/abs/2401.03568",  # Agent AI: Surveying the Horizons of Multimodal Interaction
    "https://arxiv.org/abs/2401.05946",  # Learning Cognitive Maps from Transformer Representations for Efficient Planning in Partially Observed Environments
    "https://arxiv.org/abs/2401.07629",  # Fine-Grained Prototypes Distillation for Few-Shot Object Detection
    "https://arxiv.org/abs/2401.08190",  # MARIO: MAth Reasoning with code Interpreter Output -- A Reproducible Pipeline
    "https://arxiv.org/abs/2401.08399",  # TACO: Benchmarking Generalizable Bimanual Tool-ACtion-Object Understanding
    "https://arxiv.org/abs/2401.08541",  # Scalable Pre-training of Large Autoregressive Image Models
    "https://arxiv.org/abs/2401.09865",  # Improving fine-grained understanding in image-text pre-training
    "https://arxiv.org/abs/2401.09985",  # WorldDreamer: Towards General World Models for Video Generation via Predicting Masked Tokens
    "https://arxiv.org/abs/2401.10020",  # Self-Rewarding Language Models
    "https://arxiv.org/abs/2401.12168",  # SpatialVLM: Endowing Vision-Language Models with Spatial Reasoning Capabilities
    "https://arxiv.org/abs/2401.13987",  # Cross-Domain Few-Shot Learning via Adaptive Transformer Networks
    "https://arxiv.org/abs/2401.15318",  # Gaussian Splashing: Unified Particles for Versatile Motion Synthesis and Rendering
    "https://arxiv.org/abs/2401.15977",  # Motion-I2V: Consistent and Controllable Image-to-Video Generation with Explicit Motion Modeling
    "https://arxiv.org/abs/2401.16650",  # Augmenting Replay in World Models for Continual Reinforcement Learning
    "https://arxiv.org/abs/2401.16663",  # VR-GS: A Physical Dynamics-Aware Interactive Gaussian Splatting System in Virtual Reality
    "https://arxiv.org/abs/2401.17500",  # LeTO: Learning Constrained Visuomotor Policy with Differentiable Trajectory Optimization
    "https://arxiv.org/abs/2401.17981",  # From Training-Free to Adaptive: Empirical Insights into MLLMs' Understanding of Detection Information
    "https://arxiv.org/abs/2402.00253",  # A Survey on Hallucination in Large Vision-Language Models
    "https://arxiv.org/abs/2402.02242",  # Parameter-Efficient Fine-Tuning for Pre-Trained Vision Models: A Survey and Benchmark
    "https://arxiv.org/abs/2402.02500",  # Point Cloud Matters: Rethinking the Impact of Different Observation Spaces on Robot Learning
    "https://arxiv.org/abs/2402.03162",  # Direct-a-Video: Customized Video Generation with User-Directed Camera Movement and Object Motion
    "https://arxiv.org/abs/2402.04236",  # CogCoM: A Visual Language Model with Chain-of-Manipulations Reasoning
    "https://arxiv.org/abs/2402.06912",  # Solving Deep Reinforcement Learning Tasks with Evolution Strategies and Linear Policy Networks
    "https://arxiv.org/abs/2402.07927",  # A Systematic Survey of Prompt Engineering in Large Language Models: Techniques and Applications
    "https://arxiv.org/abs/2402.08191",  # THE COLOSSEUM: A Benchmark for Evaluating Generalization for Robotic Manipulation
    "https://arxiv.org/abs/2402.10093",  # MIM-Refiner: A Contrastive Learning Boost from Intermediate Pre-Trained Representations
    "https://arxiv.org/abs/2402.10329",  # Universal Manipulation Interface: In-The-Wild Robot Teaching Without In-The-Wild Robots
    "https://arxiv.org/abs/2402.12479",  # In value-based deep reinforcement learning, a pruned network is a good network
    "https://arxiv.org/abs/2402.13349",  # Aria Everyday Activities Dataset
    "https://arxiv.org/abs/2402.14976",  # Unsupervised Domain Adaptation within Deep Foundation Latent Spaces
    "https://arxiv.org/abs/2402.15109",  # Remaining-data-free Machine Unlearning by Suppressing Sample Contribution
    "https://arxiv.org/abs/2402.15116",  # Large Multimodal Agents: A Survey
    "https://arxiv.org/abs/2402.15391",  # Genie: Generative Interactive Environments
    "https://arxiv.org/abs/2402.15487",  # RoboEXP: Action-Conditioned Scene Graph via Interactive Exploration for Robotic Manipulation
    "https://arxiv.org/abs/2402.19161",  # MemoNav: Working Memory Model for Visual Navigation
    "https://arxiv.org/abs/2402.19249",  # Mirage: Cross-Embodiment Zero-Shot Policy Transfer with Cross-Painting
    "https://arxiv.org/abs/2403.00504",  # Learning and Leveraging World Models in Visual Representation Learning
    "https://arxiv.org/abs/2403.01299",  # A Photonic Physically Unclonable Function's Resilience to Multiple-Valued Machine Learning Attacks
    "https://arxiv.org/abs/2403.01753",  # Training-Free Pretrained Model Merging
    "https://arxiv.org/abs/2403.02334",  # Gradient Correlation Subspace Learning against Catastrophic Forgetting
    "https://arxiv.org/abs/2403.03421",  # LEAD: Learning Decomposition for Source-free Universal Domain Adaptation
    "https://arxiv.org/abs/2403.03949",  # Reconciling Reality through Simulation: A Real-to-Sim-to-Real Approach for Robust Manipulation
    "https://arxiv.org/abs/2403.03954",  # 3D Diffusion Policy: Generalizable Visuomotor Policy Learning via Simple 3D Representations
    "https://arxiv.org/abs/2403.04253",  # Mastering Memory Tasks with World Models
    "https://arxiv.org/abs/2403.06845",  # DriveDreamer-2: LLM-Enhanced World Models for Diverse Driving Video Generation
    "https://arxiv.org/abs/2403.07392",  # ViT-CoMer: Vision Transformer with Convolutional Multi-scale Feature Interaction for Dense Predictions
    "https://arxiv.org/abs/2403.07420",  # DragAnything: Motion Control for Anything using Entity Representation
    "https://arxiv.org/abs/2403.07788",  # DexCap: Scalable and Portable Mocap Data Collection System for Dexterous Manipulation
    "https://arxiv.org/abs/2403.08321",  # ManiGaussian: Dynamic Gaussian Splatting for Multi-task Robotic Manipulation
    "https://arxiv.org/abs/2403.08716",  # DIFFTACTILE: A Physics-based Differentiable Tactile Simulator for Contact-rich Robotic Manipulation
    "https://arxiv.org/abs/2403.09227",  # BEHAVIOR-1K: A Human-Centered, Embodied AI Benchmark with 1,000 Everyday Activities and Realistic Simulation
    "https://arxiv.org/abs/2403.09629",  # Quiet-STaR: Language Models Can Teach Themselves to Think Before Speaking
    "https://arxiv.org/abs/2403.09631",  # 3D-VLA: A 3D Vision-Language-Action Generative World Model
    "https://arxiv.org/abs/2403.09841",  # MultiGripperGrasp: A Dataset for Robotic Grasping from Parallel Jaw Grippers to Dexterous Hands
    "https://arxiv.org/abs/2403.10191",  # Generative Region-Language Pretraining for Open-Ended Object Detection
    "https://arxiv.org/abs/2403.10506",  # HumanoidBench: Simulated Humanoid Benchmark for Whole-Body Locomotion and Manipulation
    "https://arxiv.org/abs/2403.11999",  # HIRI-ViT: Scaling Vision Transformer with High Resolution Inputs
    "https://arxiv.org/abs/2403.12488",  # DetToolChain: A New Prompting Paradigm to Unleash Detection Ability of MLLM
    "https://arxiv.org/abs/2403.12884",  # HYDRA: A Hyper Agent for Dynamic Compositional Visual Reasoning
    "https://arxiv.org/abs/2403.12945",  # DROID: A Large-Scale In-The-Wild Robot Manipulation Dataset
    "https://arxiv.org/abs/2403.12966",  # Chain-of-Spot: Interactive Reasoning Improves Large Vision-Language Models
    "https://arxiv.org/abs/2403.13043",  # When Do We Not Need Larger Vision Models?
    "https://arxiv.org/abs/2403.13187",  # Evolutionary Optimization of Model Merging Recipes
    "https://arxiv.org/abs/2403.13257",  # Arcee's MergeKit: A Toolkit for Merging Large Language Models
    "https://arxiv.org/abs/2403.13298",  # Rotary Position Embedding for Vision Transformer
    "https://arxiv.org/abs/2403.13358",  # GeRM: A Generalist Robotic Model with Mixture-of-experts for Quadruped Robot
    "https://arxiv.org/abs/2403.14404",  # Physics-Informed Diffusion Models
    "https://arxiv.org/abs/2403.14410",  # GLC++: Source-Free Universal Domain Adaptation through Global-Local Clustering and Contrastive Affinity Learning
    "https://arxiv.org/abs/2403.14608",  # Parameter-Efficient Fine-Tuning for Large Models: A Comprehensive Survey
    "https://arxiv.org/abs/2403.15249",  # Spectral Motion Alignment for Video Motion Transfer using Diffusion Models
    "https://arxiv.org/abs/2403.16967",  # Visual Whole-Body Control for Legged Loco-Manipulation
    "https://arxiv.org/abs/2403.16999",  # Visual CoT: Advancing Multi-Modal Language Models with a Comprehensive Dataset and Benchmark for Chain-of-Thought Reasoning
    "https://arxiv.org/abs/2403.17367",  # RoboDuet: Learning a Cooperative Policy for Whole-body Legged Loco-Manipulation
    "https://arxiv.org/abs/2403.17920",  # TC4D: Trajectory-Conditioned Text-to-4D Generation
    "https://arxiv.org/abs/2403.18293",  # Efficient Test-Time Adaptation of Vision-Language Models
    "https://arxiv.org/abs/2403.18361",  # ViTAR: Vision Transformer with Any Resolution
    "https://arxiv.org/abs/2403.19103",  # Automated Black-box Prompt Engineering for Personalized Text-to-Image Generation
    "https://arxiv.org/abs/2403.19417",  # OAKINK2: A Dataset of Bimanual Hands-Object Manipulation in Complex Task Completion
    "https://arxiv.org/abs/2403.19622",  # RH20T-P: A Primitive-Level Robotic Dataset Towards Composable Generalization Agents
    "https://arxiv.org/abs/2403.20193",  # Motion Inversion for Video Customization
    "https://arxiv.org/abs/2404.00756",  # Recover: A Neuro-Symbolic Framework for Failure Detection and Recovery
    "https://arxiv.org/abs/2404.01223",  # Feature Splatting: Language-Driven Physics-Based Scene Synthesis and Editing
    "https://arxiv.org/abs/2404.03622",  # Mind's Eye of LLMs: Visualization-of-Thought Elicits Spatial Reasoning in Large Language Models
    "https://arxiv.org/abs/2404.04452",  # Vision transformers in domain adaptation and domain generalization: a study of robustness
    "https://arxiv.org/abs/2404.05014",  # MagicTime: Time-lapse Video Generation Models as Metamorphic Simulators
    "https://arxiv.org/abs/2404.07664",  # Finding Dino: A Plug-and-Play Framework for Zero-Shot Detection of Out-of-Distribution Objects Using Prototypes
    "https://arxiv.org/abs/2404.08233",  # Generalized Population-Based Training for Hyperparameter Optimization in Reinforcement Learning
    "https://arxiv.org/abs/2404.08471",  # Revisiting Feature Prediction for Learning Visual Representations from Video
    "https://arxiv.org/abs/2404.09080",  # Safe Reinforcement Learning on the Constraint Manifold: Theory and Applications
    "https://arxiv.org/abs/2404.09216",  # DetCLIPv3: Towards Versatile Generative Open-vocabulary Object Detection
    "https://arxiv.org/abs/2404.09833",  # Video2Game: Real-time, Interactive, Realistic and Browser-Compatible Environment from a Single Video
    "https://arxiv.org/abs/2404.10399",  # FoundationGrasp: Generalizable Task-Oriented Grasping with Foundation Models
    "https://arxiv.org/abs/2404.12308",  # ASID: Active Exploration for System Identification in Robotic Manipulation
    "https://arxiv.org/abs/2404.13009",  # Online Policy Optimization in Unknown Nonlinear Systems
    "https://arxiv.org/abs/2404.13013",  # Groma: Localized Visual Tokenization for Grounding Multimodal Large Language Models
    "https://arxiv.org/abs/2404.13026",  # PhysDreamer: Physics-Based Interaction with 3D Objects via Video Generation
    "https://arxiv.org/abs/2404.14387",  # A Survey on Self-Evolution of Large Language Models
    "https://arxiv.org/abs/2404.14396",  # SEED-X: Multimodal Models with Unified Multi-granularity Comprehension and Generation
    "https://arxiv.org/abs/2404.15189",  # Text2Grasp: Grasp synthesis by text prompts of object grasping parts
    "https://arxiv.org/abs/2404.15617",  # A Differential and Pointwise Control Approach to Reinforcement Learning
    "https://arxiv.org/abs/2404.15817",  # Vision Transformer-based Adversarial Domain Adaptation
    "https://arxiv.org/abs/2404.16432",  # Point-JEPA: A Joint Embedding Predictive Architecture for Self-Supervised Learning on Point Cloud
    "https://arxiv.org/abs/2404.16710",  # LayerSkip: Enabling Early Exit Inference and Self-Speculative Decoding
    "https://arxiv.org/abs/2404.17202",  # Self-supervised visual learning in the low-data regime: a comparative evaluation
    "https://arxiv.org/abs/2404.18926",  # Point Cloud Models Improve Visual Robustness in Robotic Learners
    "https://arxiv.org/abs/2404.19173",  # Revisiting Reward Design and Evaluation for Robust Humanoid Standing and Walking
    "https://arxiv.org/abs/2405.01792",  # Learning Robust Autonomous Navigation and Locomotion for Wheeled-Legged Robots
    "https://arxiv.org/abs/2405.02797",  # Adapting to Distribution Shift by Visual Domain Prompt Generation
    "https://arxiv.org/abs/2405.03379",  # Reverse Forward Curriculum Learning for Extreme Sample and Demonstration Efficiency in Reinforcement Learning
    "https://arxiv.org/abs/2405.04378",  # Splat-MOVER: Multi-Stage, Open-Vocabulary Robotic Manipulation via Editable Gaussian Splatting
    "https://arxiv.org/abs/2405.05439",  # How Generalizable Is My Behavior Cloning Policy? A Statistical Approach to Trustworthy Performance Evaluation
    "https://arxiv.org/abs/2405.05941",  # Evaluating Real-World Robot Manipulation Policies in Simulation
    "https://arxiv.org/abs/2405.07060",  # Memory-Maze: Scenario Driven Visual Language Navigation Benchmark for Guiding Blind People
    "https://arxiv.org/abs/2405.07391",  # AnyRotate: Gravity-Invariant In-Hand Object Rotation with Sim-to-Real Touch
    "https://arxiv.org/abs/2405.08036",  # Potentially Optimal Joint Actions Recognition for Cooperative Multi-Agent Reinforcement Learning
    "https://arxiv.org/abs/2405.08576",  # Hearing Touch: Audio-Visual Pretraining for Contact-Rich Manipulation
    "https://arxiv.org/abs/2405.08593",  # Open-Vocabulary Object Detection via Neighboring Region Attention Alignment
    "https://arxiv.org/abs/2405.09673",  # LoRA Learns Less and Forgets Less
    "https://arxiv.org/abs/2405.09818",  # Chameleon: Mixed-Modal Early-Fusion Foundation Models
    "https://arxiv.org/abs/2405.10292",  # Fine-Tuning Large Vision-Language Models as Decision-Making Agents via Reinforcement Learning
    "https://arxiv.org/abs/2405.10739",  # Efficient Multimodal Large Language Models: A Survey
    "https://arxiv.org/abs/2405.12213",  # Octo: An Open-Source Generalist Robot Policy
    "https://arxiv.org/abs/2405.12399",  # Diffusion for World Modeling: Visual Details Matter in Atari
    "https://arxiv.org/abs/2405.12961",  # Aligning Transformers with Continuous Feedback via Energy Rank Alignment
    "https://arxiv.org/abs/2405.13532",  # What Makes Good Few-shot Examples for Vision-Language Models?
    "https://arxiv.org/abs/2405.13557",  # MotionCraft: Physics-based Zero-Shot Video Generation
    "https://arxiv.org/abs/2405.13872",  # Image-of-Thought Prompting for Visual Reasoning Refinement in Multimodal Large Language Models
    "https://arxiv.org/abs/2405.14093",  # A Survey on Vision-Language-Action Models for Embodied AI
    "https://arxiv.org/abs/2405.14838",  # From Explicit CoT to Implicit CoT: Learning to Internalize CoT Step by Step
    "https://arxiv.org/abs/2405.15056",  # ElastoGen: 4D Generative Elastodynamics
    "https://arxiv.org/abs/2405.16417",  # CRoFT: Robust Fine-Tuning with Concurrent Optimization for OOD Generalization and Open-Set OOD Detection
    "https://arxiv.org/abs/2405.16849",  # Sync4D: Video Guided Controllable Dynamics for Physics-Based 4D Generation
    "https://arxiv.org/abs/2405.17104",  # LLM-Optic: Unveiling the Capabilities of Large Language Models for Universal Visual Grounding
    "https://arxiv.org/abs/2405.17418",  # A Self-Correcting Vision-Language-Action Model for Fast and Slow System Manipulation
    "https://arxiv.org/abs/2405.18392",  # Scaling Laws and Compute-Optimal Training Beyond Fixed Training Durations
    "https://arxiv.org/abs/2405.18418",  # Hierarchical World Models as Visual Whole-Body Humanoid Controllers
    "https://arxiv.org/abs/2405.19291",  # Grasp as You Say: Language-guided Dexterous Grasp Generation
    "https://arxiv.org/abs/2405.19334",  # LLMs Meet Multimodal Generation and Editing: A Survey
    "https://arxiv.org/abs/2405.19783",  # Instruction-Guided Visual Masking
    "https://arxiv.org/abs/2405.19988",  # Video-Language Critic: Transferable Reward Functions for Language-Conditioned Robotics
    "https://arxiv.org/abs/2405.20222",  # MOFA-Video: Controllable Image Animation via Generative Motion Field Adaptions in Frozen Image-to-Video Diffusion Model
    "https://arxiv.org/abs/2406.01188",  # UniAnimate: Taming Unified Video Diffusion Models for Consistent Human Image Animation
    "https://arxiv.org/abs/2406.01476",  # DreamPhysics: Learning Physics-Based 3D Dynamics with Video Diffusion Priors
    "https://arxiv.org/abs/2406.01584",  # SpatialRGPT: Grounded Spatial Reasoning in Vision Language Models
    "https://arxiv.org/abs/2406.01920",  # CODE: Contrasting Self-generated Description to Combat Hallucination in Large Multi-modal Models
    "https://arxiv.org/abs/2406.01967",  # DrEureka: Language Model Guided Sim-To-Real Transfer
    "https://arxiv.org/abs/2406.02523",  # RoboCasa: Large-Scale Simulation of Everyday Tasks for Generalist Robots
    "https://arxiv.org/abs/2406.02537",  # TopViewRS: Vision-Language Models as Top-View Spatial Reasoners
    "https://arxiv.org/abs/2406.03303",  # Learning Visual Prompts for Guiding the Attention of Vision Transformers
    "https://arxiv.org/abs/2406.03520",  # VideoPhy: Evaluating Physical Commonsense for Video Generation
    "https://arxiv.org/abs/2406.03813",  # Touch100k: A Large-Scale Touch-Language-Vision Dataset for Touch-Centric Multimodal Representation
    "https://arxiv.org/abs/2406.03816",  # ReST-MCTS*: LLM Self-Training via Process Reward Guided Tree Search
    "https://arxiv.org/abs/2406.03862",  # Robust Deep Reinforcement Learning against Adversarial Behavior Manipulation
    "https://arxiv.org/abs/2406.04151",  # AgentGym: Evolving Large Language Model-based Agents across Diverse Environments
    "https://arxiv.org/abs/2406.04155",  # Improving Physics-Augmented Continuum Neural Radiance Field-Based Geometry-Agnostic System Identification with Lagrangian Particle Optimization
    "https://arxiv.org/abs/2406.04338",  # Physics3D: Learning Physical Properties of 3D Gaussians via Video Diffusion
    "https://arxiv.org/abs/2406.04339",  # RoboMamba: Efficient Vision-Language-Action Model for Robotic Reasoning and Manipulation
    "https://arxiv.org/abs/2406.04835",  # SLR: Learning Quadruped Locomotion without Privileged Information
    "https://arxiv.org/abs/2406.06592",  # Improve Mathematical Reasoning in Language Models by Automated Process Supervision
    "https://arxiv.org/abs/2406.07145",  # Failures Are Fated, But Can Be Faded: Characterizing and Mitigating Unwanted Behaviors in Large-Scale Vision and Language Models
    "https://arxiv.org/abs/2406.09246",  # OpenVLA: An Open-Source Vision-Language-Action Model
    "https://arxiv.org/abs/2406.09294",  # You Don't Need Domain-Specific Data Augmentations When Scaling Self-Supervised Learning
    "https://arxiv.org/abs/2406.09308",  # Transformers meet Neural Algorithmic Reasoners
    "https://arxiv.org/abs/2406.09403",  # Visual Sketchpad: Sketching as a Visual Chain of Thought for Multimodal Language Models
    "https://arxiv.org/abs/2406.09905",  # Nymeria: A Massive Collection of Multimodal Egocentric Daily Motion in the Wild
    "https://arxiv.org/abs/2406.09976",  # Robust Model-Based Reinforcement Learning with an Adversarial Auxiliary Model
    "https://arxiv.org/abs/2406.10759",  # Humanoid Parkour Learning
    "https://arxiv.org/abs/2406.10788",  # Physically Embodied Gaussian Splatting: A Realtime Correctable World Model for Robotics
    "https://arxiv.org/abs/2406.10973",  # ExPLoRA: Parameter-Efficient Extended Pre-Training to Adapt Vision Transformers under Domain Shifts
    "https://arxiv.org/abs/2406.11548",  # AIC MLLM: Autonomous Interactive Correction MLLM for Robust Robotic Manipulation
    "https://arxiv.org/abs/2406.11802",  # PhyBench: A Physical Commonsense Benchmark for Evaluating Text-to-Image Models
    "https://arxiv.org/abs/2406.12769",  # Latent Intuitive Physics: Learning to Transfer Hidden Physics from A 3D Video
    "https://arxiv.org/abs/2406.12913",  # T-JEPA: A Joint-Embedding Predictive Architecture for Trajectory Similarity Computation
    "https://arxiv.org/abs/2406.13301",  # ARDuP: Active Region Video Diffusion for Universal Policies
    "https://arxiv.org/abs/2406.13640",  # Transferable Tactile Transformers for Representation Learning Across Diverse Sensors and Tasks
    "https://arxiv.org/abs/2406.14830",  # CLIP-Decoder : ZeroShot Multilabel Classification using Multimodal CLIP Aligned Representation
    "https://arxiv.org/abs/2406.14852",  # Is A Picture Worth A Thousand Words? Delving Into Spatial Reasoning for Vision Language Models
    "https://arxiv.org/abs/2406.15339",  # Image Conductor: Precision Control for Interactive Video Synthesis
    "https://arxiv.org/abs/2406.15349",  # NAVSIM: Data-Driven Non-Reactive Autonomous Vehicle Simulation and Benchmarking
    "https://arxiv.org/abs/2406.15917",  # To Err is Robotic: Rapid Value-Based Trial-and-Error during Deployment
    "https://arxiv.org/abs/2406.16862",  # Dreamitate: Real-World Visuomotor Policy Learning via Video Generation
    "https://arxiv.org/abs/2406.17639",  # Mitigate the Gap: Investigating Approaches for Improving Cross-Modal Alignment in CLIP
    "https://arxiv.org/abs/2406.17768",  # EXTRACT: Efficient Policy Learning by Extracting Transferable Robot Skills from Offline Data
    "https://arxiv.org/abs/2406.18505",  # Mental Modeling of Reinforcement Learning Agents by Language Models
    "https://arxiv.org/abs/2406.18522",  # ChronoMagic-Bench: A Benchmark for Metamorphic Evaluation of Text-to-Time-lapse Video Generation
    "https://arxiv.org/abs/2406.18925",  # Selective Vision is the Challenge for Visual Reasoning: A Benchmark for Visual Argument Understanding
    "https://arxiv.org/abs/2406.19934",  # From the Least to the Most: Building a Plug-and-Play Visual Reasoner via Data Synthesis
    "https://arxiv.org/abs/2407.00278",  # PerAct2: Benchmarking and Learning for Robotic Bimanual Manipulation Tasks
    "https://arxiv.org/abs/2407.01400",  # GalLoP: Learning Global and Local Prompts for Vision-Language Models
    "https://arxiv.org/abs/2407.01570",  # Ego-Foresight: Self-supervised Learning of Agent-Aware Representations for Improved RL
    "https://arxiv.org/abs/2407.03475",  # How JEPA Avoids Noisy Features: The Implicit Bias of Deep Linear Self Distillation Networks
    "https://arxiv.org/abs/2407.04224",  # PA-LOCO: Learning Perturbation-Adaptive Locomotion for Quadruped Robots
    "https://arxiv.org/abs/2407.04942",  # FOSP: Fine-tuning Offline Safe Policy through World Models
    "https://arxiv.org/abs/2407.05530",  # This&That: Language-Gesture Controlled Video Generation for Robot Planning
    "https://arxiv.org/abs/2407.05996",  # Multimodal Diffusion Transformer: Learning Versatile Behavior from Multimodal Goals
    "https://arxiv.org/abs/2407.06135",  # ANOLE: An Open, Autoregressive, Native Large Multimodal Models for Interleaved Image-Text Generation
    "https://arxiv.org/abs/2407.06886",  # Aligning Cyber Space with Physical World: A Comprehensive Survey on Embodied AI
    "https://arxiv.org/abs/2407.07726",  # PaliGemma: A versatile 3B VLM for transfer
    "https://arxiv.org/abs/2407.07788",  # BiGym: A Demo-Driven Mobile Bi-Manual Manipulation Benchmark
    "https://arxiv.org/abs/2407.07889",  # AdaptiGraph: Material-Adaptive Graph-Based Neural Dynamics for Robotic Manipulation
    "https://arxiv.org/abs/2407.08028",  # AutoMate: Specialist and Generalist Assembly Policies over Diverse Geometries
    "https://arxiv.org/abs/2407.08693",  # Robotic Control via Embodied Chain-of-Thought Reasoning
    "https://arxiv.org/abs/2407.08735",  # Real-Time Anomaly Detection and Reactive Planning with Large Language Models
    "https://arxiv.org/abs/2407.10353",  # UMI on Legs: Making Manipulation Policies Mobile with Manipulation-Centric Whole-body Controllers
    "https://arxiv.org/abs/2407.10490",  # Learning Dynamics of LLM Finetuning
    "https://arxiv.org/abs/2407.11464",  # Crowd-SAM: SAM as a Smart Annotator for Object Detection in Crowded Scenes
    "https://arxiv.org/abs/2407.13771",  # Training-Free Model Merging for Multi-target Domain Adaptation
    "https://arxiv.org/abs/2407.14414",  # System-1.x: Learning to Balance Fast and Slow Planning with Language Models
    "https://arxiv.org/abs/2407.15002",  # GET-Zero: Graph Embodiment Transformer for Zero-shot Embodiment Generalization
    "https://arxiv.org/abs/2407.15173",  # Rethinking Domain Adaptation and Generalization in the Era of CLIP
    "https://arxiv.org/abs/2407.15208",  # Flow as the Cross-Domain Manipulation Interface
    "https://arxiv.org/abs/2407.16677",  # From Imitation to Refinement -- Residual RL for Precise Assembly
    "https://arxiv.org/abs/2407.17348",  # DexGANGrasp: Dexterous Generative Adversarial Grasping Synthesis for Task-Oriented Manipulation
    "https://arxiv.org/abs/2407.18834",  # Learning a Shape-Conditioned Agent for Purely Tactile In-Hand Manipulation of Various Objects
    "https://arxiv.org/abs/2407.19666",  # Take A Step Back: Rethinking the Two Stages in Visual Reasoning
    "https://arxiv.org/abs/2407.20230",  # SAPG: Split and Aggregate Policy Gradients
    "https://arxiv.org/abs/2407.21311",  # EUDA: An Efficient Unsupervised Domain Adaptation via Self-Supervised Vision Transformer
    "https://arxiv.org/abs/2407.21705",  # Tora: Trajectory-oriented Diffusion Transformer for Video Generation
    "https://arxiv.org/abs/2408.00342",  # MuJoCo MPC for Humanoid Control: Evaluation on HumanoidBench
    "https://arxiv.org/abs/2408.02272",  # COM Kitchens: An Unedited Overhead-view Video Dataset as a Vision-Language Benchmark
    "https://arxiv.org/abs/2408.03326",  # LLaVA-OneVision: Easy Visual Task Transfer
    "https://arxiv.org/abs/2408.05107",  # Depth Helps: Improving Pre-trained RGB-based Policy with Depth Information Injection
    "https://arxiv.org/abs/2408.05674",  # PS-TTL: Prototype-based Soft-labels and Test-Time Learning for Few-shot Object Detection
    "https://arxiv.org/abs/2408.05804",  # A Single Goal is All You Need: Skills and Exploration Emerge from Contrastive RL without Rewards, Demonstrations, or Subgoals
    "https://arxiv.org/abs/2408.06506",  # TacSL: A Library for Visuotactile Sensor Simulation and Learning
    "https://arxiv.org/abs/2408.07009",  # Imagen 3
    "https://arxiv.org/abs/2408.07666",  # Model Merging in LLMs, MLLMs, and Beyond: Methods, Theories, Applications and Opportunities
    "https://arxiv.org/abs/2408.08252",  # Derivative-Free Guidance in Continuous and Discrete Diffusion Models with Soft Value-Based Decoding
    "https://arxiv.org/abs/2408.10453",  # Kubrick: Multimodal Agent Collaborations for Synthetic Video Generation
    "https://arxiv.org/abs/2408.10787",  # Lightweight Modular Parameter-Efficient Tuning for Open-Vocabulary Object Detection
    "https://arxiv.org/abs/2408.10858",  # Centralized Reward Agent for Knowledge Sharing and Transfer in Multi-Task Reinforcement Learning
    "https://arxiv.org/abs/2408.10899",  # All Robots in One: A New Standard and Unified Dataset for Versatile, General-Purpose Embodied Agents
    "https://arxiv.org/abs/2408.11039",  # Transfusion: Predict the Next Token and Diffuse Images with One Multi-Modal Model
    "https://arxiv.org/abs/2408.11475",  # TrackGo: A Flexible and Efficient Method for Controllable Video Generation
    "https://arxiv.org/abs/2408.12528",  # Show-o: One Single Transformer to Unify Multimodal Understanding and Generation
    "https://arxiv.org/abs/2408.13296",  # The Ultimate Guide to Fine-Tuning LLMs from Basics to Breakthroughs: An Exhaustive Review of Technologies, Research, Best Practices, Applied Research Challenges and Opportunities
    "https://arxiv.org/abs/2408.14368",  # GR-MG: Leveraging Partially Annotated Data via Multi-Modal Goal-Conditioned Policy
    "https://arxiv.org/abs/2408.14371",  # SelEx: Self-Expertise in Fine-Grained Generalized Category Discovery
    "https://arxiv.org/abs/2408.14472",  # Advancing Humanoid Locomotion: Mastering Challenging Terrains with Denoising World Model Learning
    "https://arxiv.org/abs/2408.14837",  # Diffusion Models Are Real-Time Game Engines
    "https://arxiv.org/abs/2408.15240",  # Generative Verifiers: Reward Modeling as Next-Token Prediction
    "https://arxiv.org/abs/2408.15332",  # What makes math problems hard for reinforcement learning: a case study
    "https://arxiv.org/abs/2408.15511",  # AeroVerse: UAV-Agent Benchmark Suite for Simulating, Pre-training, Finetuning, and Evaluating Aerospace Embodied World Models
    "https://arxiv.org/abs/2408.16662",  # Space3D-Bench: Spatial 3D Question Answering Benchmark
    "https://arxiv.org/abs/2408.17059",  # A Survey of the Self Supervised Learning Mechanisms for Vision Transformers
    "https://arxiv.org/abs/2409.00215",  # Constraint-Aware Intent Estimation for Dynamic Human-Robot Object Co-Manipulation
    "https://arxiv.org/abs/2409.00558",  # Compositional 3D-aware Video Generation with LLM Director
    "https://arxiv.org/abs/2409.00872",  # Self-evolving Agents with reflective and memory-augmented abilities
    "https://arxiv.org/abs/2409.01652",  # ReKep: Spatio-Temporal Reasoning of Relational Keypoint Constraints for Robotic Manipulation
    "https://arxiv.org/abs/2409.02561",  # Vision-Language Navigation with Continual Learning
    "https://arxiv.org/abs/2409.03299",  # Bringing the RT-1-X Foundation Model to a SCARA robot
    "https://arxiv.org/abs/2409.03966",  # Automating Robot Failure Recovery Using Vision-Language Models With Optimized Prompts
    "https://arxiv.org/abs/2409.04429",  # VILA-U: a Unified Foundation Model Integrating Visual Understanding and Generation
    "https://arxiv.org/abs/2409.07179",  # Phy124: Fast Physics-Driven 4D Content Generation from a Single Image
    "https://arxiv.org/abs/2409.07914",  # InterACT: Inter-dependency Aware Action Chunking with Hierarchical Attention Transformers for Bimanual Manipulation
    "https://arxiv.org/abs/2409.10161",  # SplatSim: Zero-Shot Sim2Real Transfer of RGB Manipulation Policies Using Gaussian Splatting
    "https://arxiv.org/abs/2409.12514",  # TinyVLA: Towards Fast, Data-Efficient Vision-Language-Action Models for Robotic Manipulation
    "https://arxiv.org/abs/2409.14401",  # Investigating the Impact of Hard Samples on Accuracy Reveals In-class Data Imbalance
    "https://arxiv.org/abs/2409.14507",  # A is for Absorption: Studying Feature Splitting and Absorption in Sparse Autoencoders
    "https://arxiv.org/abs/2409.15310",  # Visual Prompting in Multimodal Large Language Models: A Survey
    "https://arxiv.org/abs/2409.15803",  # 3D-JEPA: A Joint Embedding Predictive Architecture for 3D Self-Supervised Representation Learning
    "https://arxiv.org/abs/2409.16048",  # Whole-body End-Effector Pose Tracking
    "https://arxiv.org/abs/2409.16283",  # Gen2Act: Human Video Generation in Novel Scenarios enables Generalizable Robot Manipulation
    "https://arxiv.org/abs/2409.16578",  # FLaRe: Achieving Masterful and Adaptive Robot Policies with Large-Scale Reinforcement Learning Fine-Tuning
    "https://arxiv.org/abs/2409.16784",  # World Model-based Perception for Visual Legged Locomotion
    "https://arxiv.org/abs/2409.17146",  # Molmo and PixMo: Open Weights and Open Data for State-of-the-Art Vision-Language Models
    "https://arxiv.org/abs/2409.17411",  # Enhancing Interpretability in Deep Reinforcement Learning through Semantic Clustering
    "https://arxiv.org/abs/2409.17992",  # LoopSR: Looping Sim-and-Real for Lifelong Policy Adaptation of Legged Robots
    "https://arxiv.org/abs/2409.18313",  # Embodied-RAG: General Non-parametric Embodied Memory for Retrieval and Generation
    "https://arxiv.org/abs/2409.18330",  # DMC-VB: A Benchmark for Representation Learning for Control with Visual Distractors
    "https://arxiv.org/abs/2409.18869",  # Emu3: Next-Token Prediction is All You Need
    "https://arxiv.org/abs/2409.18964",  # PhysGen: Rigid-Body Physics-Grounded Image-to-Video Generation
    "https://arxiv.org/abs/2409.19190",  # RAIL: Reachability-Aided Imitation Learning for Safe Policy Execution
    "https://arxiv.org/abs/2409.19499",  # FastUMI: A Scalable and Hardware-Independent Universal Manipulation Interface with Dataset
    "https://arxiv.org/abs/2409.20291",  # RL-GSBridge: 3D Gaussian Splatting Based Real2Sim2Real Method for Robotic Manipulation Learning
    "https://arxiv.org/abs/2409.20514",  # Opt2Skill: Imitating Dynamically-feasible Whole-Body Trajectories for Versatile Humanoid Loco-Manipulation
    "https://arxiv.org/abs/2409.20537",  # Scaling Proprioceptive-Visual Learning with Heterogeneous Pre-trained Transformers
    "https://arxiv.org/abs/2410.00371",  # AHA: A Vision-Language-Model for Detecting and Reasoning Over Failures in Robotic Manipulation
    "https://arxiv.org/abs/2410.00425",  # ManiSkill3: GPU Parallelized Robotics Simulation and Rendering for Generalizable Embodied AI
    "https://arxiv.org/abs/2410.00564",  # Scaling Offline Model-Based RL via Jointly-Optimized World-Action Model Pretraining
    "https://arxiv.org/abs/2410.00841",  # Diffusion-Informed Probabilistic Contact Search for Multi-Finger Manipulation
    "https://arxiv.org/abs/2410.01345",  # Towards Generalizable Vision-Language Robotic Manipulation: A Benchmark and LLM-guided 3D Policy
    "https://arxiv.org/abs/2410.01679",  # VinePPO: Refining Credit Assignment in RL Training of LLMs
    "https://arxiv.org/abs/2410.01702",  # $\mathcal{D(R,O)}$ Grasp: A Unified Representation of Robot and Object Interaction for Cross-Embodiment Dexterous Grasping
    "https://arxiv.org/abs/2410.01735",  # LASeR: Learning to Adaptively Select Reward Models with Multi-Armed Bandits
    "https://arxiv.org/abs/2410.01968",  # Bi-Level Motion Imitation for Humanoid Robots
    "https://arxiv.org/abs/2410.02355",  # AlphaEdit: Null-Space Constrained Knowledge Editing for Language Models
    "https://arxiv.org/abs/2410.02479",  # Cross-Embodiment Dexterous Grasping with Reinforcement Learning
    "https://arxiv.org/abs/2410.02735",  # OOD-Chameleon: Is Algorithm Selection for OOD Generalization Learnable?
    "https://arxiv.org/abs/2410.02742",  # Grounding Large Language Models In Embodied Environment With Imperfect World Models
    "https://arxiv.org/abs/2410.03119",  # Spatial-Aware Decision-Making with Ring Attractors in Reinforcement Learning Systems
    "https://arxiv.org/abs/2410.03755",  # Denoising with a Joint-Embedding Predictive Architecture
    "https://arxiv.org/abs/2410.04640",  # Unpacking Failure Modes of Generative Policies: Runtime Monitoring of Consistency and Progress
    "https://arxiv.org/abs/2410.04891",  # Low-Rank Continual Personalization of Diffusion Models
    "https://arxiv.org/abs/2410.05363",  # Towards World Simulator: Crafting Physical Commonsense-Based Benchmark for Video Generation
    "https://arxiv.org/abs/2410.05582",  # Gen-Drive: Enhancing Diffusion Generative Driving Policies with Reward Modeling and Reinforcement Learning Fine-tuning
    "https://arxiv.org/abs/2410.05975",  # Learning to Learn with Contrastive Meta-Objective
    "https://arxiv.org/abs/2410.06158",  # GR-2: A Generative Video-Language-Action Model with Web-Scale Knowledge for Robot Manipulation
    "https://arxiv.org/abs/2410.06468",  # Does Spatial Cognition Emerge in Frontier Models?
    "https://arxiv.org/abs/2410.07155",  # Trans4D: Realistic Geometry-Aware Transition for Compositional Text-to-4D Synthesis
    "https://arxiv.org/abs/2410.07170",  # Parameter Efficient Fine-tuning via Explained Variance Adaptation
    "https://arxiv.org/abs/2410.07408",  # Automated Creation of Digital Cousins for Robust Policy Learning
    "https://arxiv.org/abs/2410.07812",  # Temporal-Difference Variational Continual Learning
    "https://arxiv.org/abs/2410.07864",  # RDT-1B: a Diffusion Foundation Model for Bimanual Manipulation
    "https://arxiv.org/abs/2410.08021",  # OneRef: Unified One-tower Expression Grounding and Segmentation with Mask Referring Modeling
    "https://arxiv.org/abs/2410.08146",  # Rewarding Progress: Scaling Automated Process Verifiers for LLM Reasoning
    "https://arxiv.org/abs/2410.08202",  # Mono-InternVL: Pushing the Boundaries of Monolithic Multimodal Large Language Models with Endogenous Visual Pre-training
    "https://arxiv.org/abs/2410.08257",  # Neural Material Adaptor for Visual Grounding of Intrinsic Dynamics
    "https://arxiv.org/abs/2410.08328",  # Agents Thinking Fast and Slow: A Talker-Reasoner Architecture
    "https://arxiv.org/abs/2410.08655",  # FRASA: An End-to-End Reinforcement Learning Agent for Fall Recovery and Stand Up of Humanoid Robots
    "https://arxiv.org/abs/2410.10076",  # VideoAgent: Self-Improving Video Generation
    "https://arxiv.org/abs/2410.10101",  # Learning Linear Attention in Polynomial Time
    "https://arxiv.org/abs/2410.10855",  # Core Knowledge Deficits in Multi-Modal Language Models
    "https://arxiv.org/abs/2410.11234",  # Bayes Adaptive Monte Carlo Tree Search for Offline Model-based Reinforcement Learning
    "https://arxiv.org/abs/2410.11758",  # Latent Action Pretraining from Videos
    "https://arxiv.org/abs/2410.11834",  # Contrastive Touch-to-Touch Pretraining
    "https://arxiv.org/abs/2410.11989",  # Dynamic Open-Vocabulary 3D Scene Graphs for Long-term Language-Guided Mobile Manipulation
    "https://arxiv.org/abs/2410.12735",  # CREAM: Consistency Regularized Self-Rewarding Language Models
    "https://arxiv.org/abs/2410.13571",  # DriveDreamer4D: World Models Are Effective Data Machines for 4D Driving Scene Representation
    "https://arxiv.org/abs/2410.13733",  # Improving Multi-modal Large Language Model through Boosting Vision Capabilities
    "https://arxiv.org/abs/2410.13830",  # DreamVideo-2: Zero-Shot Subject-Driven Video Customization with Precise Motion Control
    "https://arxiv.org/abs/2410.13842",  # D-FINE: Redefine Regression Task in DETRs as Fine-grained Distribution Refinement
    "https://arxiv.org/abs/2410.13848",  # Janus: Decoupling Visual Encoding for Unified Multimodal Understanding and Generation
    "https://arxiv.org/abs/2410.14868",  # Diff-DAgger: Uncertainty Estimation with Diffusion Policy for Robotic Manipulation
    "https://arxiv.org/abs/2410.15639",  # Can Large Language Models Invent Algorithms to Improve Themselves?: Algorithm Discovery for Recursive Self-Improvement through Reinforcement Learning
    "https://arxiv.org/abs/2410.15959",  # Diffusion Transformer Policy
    "https://arxiv.org/abs/2410.16392",  # Scaffolded Language Models with Language Supervision for Mixed-Autonomy: A Survey
    "https://arxiv.org/abs/2410.16400",  # VipAct: Visual-Perception Enhancement via Specialized VLM Agent Collaboration and Tool-use
    "https://arxiv.org/abs/2410.16512",  # TIPS: Text-Image Pretraining with Spatial awareness
    "https://arxiv.org/abs/2410.17385",  # Do Vision-Language Models Represent Space and How? Evaluating Spatial Frame of Reference Under Ambiguities
    "https://arxiv.org/abs/2410.17517",  # The Hive Mind is a Single Reinforcement Learning Agent
    "https://arxiv.org/abs/2410.18072",  # WorldSimBench: Towards Video Generation Models as World Simulators
    "https://arxiv.org/abs/2410.18252",  # Asynchronous RLHF: Faster and More Efficient Off-Policy RL for Language Models
    "https://arxiv.org/abs/2410.18907",  # SkillMimicGen: Automated Demonstration Generation for Efficient Skill Learning and Deployment
    "https://arxiv.org/abs/2410.18964",  # Learning to Look: Seeking Information for Decision Making via Policy Factorization
    "https://arxiv.org/abs/2410.19560",  # Connecting Joint-Embedding Predictive Architecture with Contrastive Self-supervised Learning
    "https://arxiv.org/abs/2410.19878",  # Parameter-Efficient Fine-Tuning in Large Models: A Survey of Methodologies
    "https://arxiv.org/abs/2410.19925",  # Improving Multimodal Large Language Models Using Continual Learning
    "https://arxiv.org/abs/2410.19933",  # Enhancing Safety in Reinforcement Learning with Human Feedback via Rectified Policy Optimization
    "https://arxiv.org/abs/2410.20357",  # Dynamics as Prompts: In-Context Learning for Sim-to-Real System Identifications
    "https://arxiv.org/abs/2410.20722",  # Interpretable Image Classification with Adaptive Prototype-based Vision Transformers
    "https://arxiv.org/abs/2410.21151",  # BraVE: Offline Reinforcement Learning for Discrete Combinatorial Action Spaces
    "https://arxiv.org/abs/2410.21676",  # How Does Critical Batch Size Scale in Pre-training?
    "https://arxiv.org/abs/2410.21845",  # Precise and Dexterous Robotic Manipulation via Human-in-the-Loop Reinforcement Learning
    "https://arxiv.org/abs/2410.22325",  # Robots Pre-train Robots: Manipulation-Centric Robotic Representation from Large-Scale Robot Datasets
    "https://arxiv.org/abs/2410.22689",  # Multi-Task Interactive Robot Fleet Learning with Visual World Models
    "https://arxiv.org/abs/2410.22979",  # LumiSculpt: Enabling Consistent Portrait Lighting in Video Generation
    "https://arxiv.org/abs/2410.23223",  # COMAL: A Convergent Meta-Algorithm for Aligning LLMs with General Preferences
    "https://arxiv.org/abs/2410.24090",  # Sparsh: Self-supervised touch representations for vision-based tactile sensing
    "https://arxiv.org/abs/2410.24164",  # $π_0$: A Vision-Language-Action Flow Model for General Robot Control
    "https://arxiv.org/abs/2410.24185",  # DexMimicGen: Automated Data Generation for Bimanual Dexterous Manipulation via Imitation Learning
    "https://arxiv.org/abs/2410.24221",  # EgoMimic: Scaling Imitation Learning via Egocentric Video
    "https://arxiv.org/abs/2411.00361",  # Direct Preference Optimization for Primitive-Enabled Hierarchical RL: A Bilevel Approach
    "https://arxiv.org/abs/2411.00554",  # Differentiable Physics-based System Identification for Robotic Manipulation of Elastoplastic Materials
    "https://arxiv.org/abs/2411.00769",  # GameGen-X: Interactive Open-world Game Video Generation
    "https://arxiv.org/abs/2411.02385",  # How Far is Video Generation from World Model: A Physical Law Perspective
    "https://arxiv.org/abs/2411.02394",  # AutoVFX: Physically Realistic Video Editing from Natural Language Instructions
    "https://arxiv.org/abs/2411.04109",  # Self-Consistency Preference Optimization
    "https://arxiv.org/abs/2411.04625",  # Sharp Analysis for KL-Regularized Contextual Bandits and RLHF
    "https://arxiv.org/abs/2411.04983",  # DINO-WM: World Models on Pre-trained Visual Features enable Zero-shot Planning
    "https://arxiv.org/abs/2411.04989",  # SG-I2V: Self-Guided Trajectory Control in Image-to-Video Generation
    "https://arxiv.org/abs/2411.04997",  # LLM2CLIP: Powerful Language Model Unlocks Richer Visual Representation
    "https://arxiv.org/abs/2411.04999",  # DynaMem: Online Dynamic Spatio-Semantic Memory for Open World Mobile Manipulation
    "https://arxiv.org/abs/2411.06782",  # QuadWBG: Generalizable Quadrupedal Whole-Body Grasping
    "https://arxiv.org/abs/2411.07833",  # Robust Adaptive Safe Robotic Grasping with Tactile Sensing
    "https://arxiv.org/abs/2411.08027",  # LLMPhy: Complex Physical Reasoning Using Large Language Models and World Models
    "https://arxiv.org/abs/2411.08127",  # TIPO: Text to Image with Text Presampling for Prompt Optimization
    "https://arxiv.org/abs/2411.08380",  # EgoVid-5M: A Large-Scale Video-Action Dataset for Egocentric Video Generation
    "https://arxiv.org/abs/2411.08832",  # Offline Adaptation of Quadruped Locomotion using Diffusion Models
    "https://arxiv.org/abs/2411.09691",  # Advancing Fine-Grained Visual Understanding with Multi-Scale Alignment in Multi-Modal Models
    "https://arxiv.org/abs/2411.10231",  # A Low-Resolution Image is Worth 1x1 Words: Enabling Fine Image Super-Resolution with Transformers and TaylorShift
    "https://arxiv.org/abs/2411.10440",  # LLaVA-CoT: Let Vision Language Models Reason Step-by-Step
    "https://arxiv.org/abs/2411.10442",  # Enhancing the Reasoning Ability of Multimodal Large Language Models via Mixed Preference Optimization
    "https://arxiv.org/abs/2411.10836",  # AnimateAnything: Consistent and Controllable Animation for Video Generation
    "https://arxiv.org/abs/2411.11343",  # Latent Knowledge-Guided Video Diffusion for Scientific Phenomena Generation from a Single Initial Frame
    "https://arxiv.org/abs/2411.11839",  # RoboGSim: A Real2Sim2Real Robotic Gaussian Splatting Simulator
    "https://arxiv.org/abs/2411.11930",  # AtomThink: Multimodal Slow Thinking with Atomic Step Reasoning
    "https://arxiv.org/abs/2411.12503",  # ManiSkill-ViTac 2025: Challenge on Manipulation Skill Learning With Vision and Tactile Sensing
    "https://arxiv.org/abs/2411.12591",  # Thinking Before Looking: Improving Multimodal LLM Reasoning via Mitigating Visual Hallucination
    "https://arxiv.org/abs/2411.12789",  # Efficient Physics Simulation for 3D Scenes via MLLM-Guided Gaussian Splatting
    "https://arxiv.org/abs/2411.13587",  # Exploring the Adversarial Vulnerabilities of Vision-Language-Action Models in Robotics
    "https://arxiv.org/abs/2411.13609",  # What You See Is What Matters: A Novel Visual and Physics-Based Metric for Evaluating Video Generation Quality
    "https://arxiv.org/abs/2411.13852",  # Dealing with Synthetic Data Contamination in Online Continual Learning
    "https://arxiv.org/abs/2411.14251",  # Natural Language Reinforcement Learning
    "https://arxiv.org/abs/2411.14386",  # Learning Humanoid Locomotion with Perceptive Internal Model
    "https://arxiv.org/abs/2411.14402",  # Multimodal Autoregressive Pre-training of Large Vision Encoders
    "https://arxiv.org/abs/2411.14405",  # Marco-o1: Towards Open Reasoning Models for Open-Ended Solutions
    "https://arxiv.org/abs/2411.14423",  # PhysFlow: Unleashing the Potential of Multi-modal Foundation Models and Video Diffusion for 4D Dynamic Physical Scene Simulation
    "https://arxiv.org/abs/2411.14499",  # Understanding World or Predicting Future? A Comprehensive Survey of World Models
    "https://arxiv.org/abs/2411.15046",  # On Feasible Rewards in Multi-Agent Inverse Reinforcement Learning
    "https://arxiv.org/abs/2411.15594",  # A Survey on LLM-as-a-Judge
    "https://arxiv.org/abs/2411.15869",  # Self-Calibrated CLIP for Training-Free Open-Vocabulary Segmentation
    "https://arxiv.org/abs/2411.16044",  # ZoomEye: Enhancing Multimodal LLMs with Human-Like Zooming Capabilities through Tree-Based Image Exploration
    "https://arxiv.org/abs/2411.16755",  # FunGrasp: Functional Grasping for Diverse Dexterous Hands
    "https://arxiv.org/abs/2411.16800",  # Phys4DGen: Physics-Compliant 4D Generation with Multi-Material Composition Perception
    "https://arxiv.org/abs/2411.16804",  # InTraGen: Trajectory-controlled Video Generation for Object Interactions
    "https://arxiv.org/abs/2411.17189",  # PhysMotion: Physics-Grounded Dynamics From a Single Image
    "https://arxiv.org/abs/2411.17440",  # Identity-Preserving Text-to-Video Generation by Frequency Decomposition
    "https://arxiv.org/abs/2411.17673",  # SketchAgent: Language-Driven Sequential Sketch Generation
    "https://arxiv.org/abs/2411.17735",  # 3D-Mem: 3D Scene Memory for Embodied Exploration and Reasoning
    "https://arxiv.org/abs/2411.18179",  # Prediction with Action: Visual Policy Learning via Joint Denoising Process
    "https://arxiv.org/abs/2411.18676",  # Embodied Red Teaming for Auditing Robotic Foundation Models
    "https://arxiv.org/abs/2411.19167",  # HOT3D: Hand and Object Tracking in 3D from Egocentric Multi-View Videos
    "https://arxiv.org/abs/2411.19309",  # GRAPE: Generalizing Robot Policy via Preference Alignment
    "https://arxiv.org/abs/2411.19331",  # Talking to DINO: Bridging Self-Supervised Vision Backbones with Language for Open-Vocabulary Segmentation
    "https://arxiv.org/abs/2411.19381",  # Enhancing Sketch Animation: Text-to-Video Diffusion Models with Temporal Consistency and Rigidity Constraints
    "https://arxiv.org/abs/2411.19408",  # SoGraB: A Visual Method for Soft Grasping Benchmarking and Evaluation
    "https://arxiv.org/abs/2411.19488",  # Interleaved-Modal Chain-of-Thought
    "https://arxiv.org/abs/2411.19650",  # CogACT: A Foundational Vision-Language-Action Model for Synergizing Cognition and Action in Robotic Manipulation
    "https://arxiv.org/abs/2412.00148",  # Motion Modes: What Could Happen Next?
    "https://arxiv.org/abs/2412.00259",  # One-Shot Real-to-Sim via End-to-End Differentiable Simulation and Rendering
    "https://arxiv.org/abs/2412.00420",  # TAROT: Targeted Data Selection via Optimal Transport
    "https://arxiv.org/abs/2412.00596",  # PhyT2V: LLM-Guided Iterative Self-Refinement for Physics-Grounded Text-to-Video Generation
    "https://arxiv.org/abs/2412.00661",  # Mean-Field Sampling for Cooperative Multi-Agent Reinforcement Learning
    "https://arxiv.org/abs/2412.00798",  # Combinatorial Rising Bandits
    "https://arxiv.org/abs/2412.01282",  # Align-KD: Distilling Cross-Modal Alignment Knowledge for Mobile Vision-Language Model
    "https://arxiv.org/abs/2412.01770",  # Robot Learning with Super-Linear Scaling
    "https://arxiv.org/abs/2412.01791",  # DextrAH-RGB: Visuomotor Policies to Grasp Anything with Dexterous Hands
    "https://arxiv.org/abs/2412.01800",  # PhysGame: Uncovering Physical Commonsense Violations in Gameplay Videos
    "https://arxiv.org/abs/2412.01857",  # Planning from Imagination: Episodic Simulation and Episodic Memory for Vision-and-Language Navigation
    "https://arxiv.org/abs/2412.01951",  # Self-Improvement in Language Models: The Sharpening Mechanism
    "https://arxiv.org/abs/2412.02168",  # Generative Photography: Scene-Consistent Camera Control for Realistic Text-to-Image Synthesis
    "https://arxiv.org/abs/2412.02617",  # Improving Dynamic Object Interactions in Text-to-Video Generation with AI Feedback
    "https://arxiv.org/abs/2412.02700",  # Motion Prompting: Controlling Video Generation with Motion Trajectories
    "https://arxiv.org/abs/2412.02818",  # RoboMD: Uncovering Robot Vulnerabilities through Semantic Potential Fields
    "https://arxiv.org/abs/2412.03012",  # Learning Whole-Body Loco-Manipulation for Omni-Directional Task Space Pose Tracking with a Wheeled-Quadrupedal-Manipulator
    "https://arxiv.org/abs/2412.03069",  # TokenFlow: Unified Image Tokenizer for Multimodal Understanding and Generation
    "https://arxiv.org/abs/2412.03548",  # Perception Tokens Enhance Visual Reasoning in Multimodal Language Models
    "https://arxiv.org/abs/2412.03568",  # The Matrix: Infinite-Horizon World Generation with Real-Time Moving Control
    "https://arxiv.org/abs/2412.03572",  # Navigation World Models
    "https://arxiv.org/abs/2412.04073",  # TransAdapter: Vision Transformer for Feature-Centric Unsupervised Domain Adaptation
    "https://arxiv.org/abs/2412.04233",  # HyperMARL: Adaptive Hypernetworks for Multi-Agent RL
    "https://arxiv.org/abs/2412.04323",  # GRAM: Generalization in Deep RL with a Robust Adaptation Module
    "https://arxiv.org/abs/2412.04426",  # Towards Fast Safe Online Reinforcement Learning via Policy Finetuning
    "https://arxiv.org/abs/2412.04445",  # Moto: Latent Motion Token as the Bridging Language for Learning Robot Manipulation from Videos
    "https://arxiv.org/abs/2412.04455",  # Code-as-Monitor: Constraint-aware Visual Programming for Reactive and Proactive Robotic Failure Detection
    "https://arxiv.org/abs/2412.04468",  # NVILA: Efficient Frontier Visual Language Models
    "https://arxiv.org/abs/2412.05265",  # Reinforcement Learning: An Overview
    "https://arxiv.org/abs/2412.05313",  # λ: A Benchmark for Data-Efficiency in Long-Horizon Indoor Mobile Manipulation Robotics
    "https://arxiv.org/abs/2412.05479",  # LATTE: Learning to Think with Vision Specialists
    "https://arxiv.org/abs/2412.05718",  # RLZero: Direct Policy Inference from Language Without In-Domain Supervision
    "https://arxiv.org/abs/2412.06531",  # Unraveling the Complexity of Memory in RL Agents: an Approach for Classification and Evaluation
    "https://arxiv.org/abs/2412.06769",  # Training Large Language Models to Reason in a Continuous Latent Space
    "https://arxiv.org/abs/2412.07012",  # ProVision: Programmatically Scaling Vision-centric Instruction Data for Multimodal Language Models
    "https://arxiv.org/abs/2412.07215",  # RoboTron-Mani: All-in-One Multimodal Large Model for Robotic Manipulation
    "https://arxiv.org/abs/2412.07679",  # RADIOv2.5: Improved Baselines for Agglomerative Vision Foundation Models
    "https://arxiv.org/abs/2412.07755",  # SAT: Dynamic Spatial Aptitude Training for Multimodal Language Models
    "https://arxiv.org/abs/2412.07825",  # 3DSRBench: A Comprehensive 3D Spatial Reasoning Benchmark
    "https://arxiv.org/abs/2412.08410",  # Physical Informed Driving World Model
    "https://arxiv.org/abs/2412.08635",  # Multimodal Latent Language Modeling with Next-Token Diffusion
    "https://arxiv.org/abs/2412.09413",  # Imitate, Explore, and Self-Improve: A Reproduction Report on Slow-thinking Reasoning Systems
    "https://arxiv.org/abs/2412.09544",  # Sail into the Headwind: Alignment via Robust Rewards and Dynamic Labels against Reward Hacking
    "https://arxiv.org/abs/2412.09551",  # Video Creation by Demonstration
    "https://arxiv.org/abs/2412.09858",  # RLDG: Robotic Generalist Policy Distillation via Reinforcement Learning
    "https://arxiv.org/abs/2412.10345",  # TraceVLA: Visual Trace Prompting Enhances Spatial-Temporal Awareness for Generalist Robotic Policies
    "https://arxiv.org/abs/2412.10439",  # CogNav: Cognitive Process Modeling for Object Goal Navigation with LLMs
    "https://arxiv.org/abs/2412.10713",  # RAT: Adversarial Attacks on Deep Reinforcement Agents for Targeted Behaviors
    "https://arxiv.org/abs/2412.10908",  # Do large language vision models understand 3D shapes?
    "https://arxiv.org/abs/2412.11224",  # GenLit: Reformulating Single-Image Relighting as Video Generation
    "https://arxiv.org/abs/2412.11258",  # GaussianProperty: Integrating Physical Properties to 3D Gaussians with LMMs
    "https://arxiv.org/abs/2412.11785",  # InterDyn: Controllable Interactive Dynamics with Video Diffusion Models
    "https://arxiv.org/abs/2412.11974",  # Emma-X: An Embodied Multimodal Action Model with Grounded Chain of Thought and Look-ahead Spatial Reasoning
    "https://arxiv.org/abs/2412.11979",  # AlphaZero Neural Scaling and Zipf's Law: a Tale of Board Games and Power Laws
    "https://arxiv.org/abs/2412.13171",  # Compressed Chain of Thought: Efficient Reasoning Through Dense Representations
    "https://arxiv.org/abs/2412.13211",  # ManiSkill-HAB: A Benchmark for Low-Level Manipulation in Home Rearrangement Tasks
    "https://arxiv.org/abs/2412.13303",  # FastVLM: Efficient Vision Encoding for Vision Language Models
    "https://arxiv.org/abs/2412.13810",  # CAD-Assistant: Tool-Augmented VLLMs as Generic CAD Task Solvers
    "https://arxiv.org/abs/2412.13871",  # LLaVA-UHD v2: an MLLM Integrating High-Resolution Semantic Pyramid via Hierarchical Window Transformer
    "https://arxiv.org/abs/2412.13877",  # RoboMIND: Benchmark on Multi-embodiment Intelligence Normative Data for Robot Manipulation
    "https://arxiv.org/abs/2412.14058",  # What Matters in Building Vision-Language-Action Models for Generalist Robots
    "https://arxiv.org/abs/2412.14123",  # AnySat: One Earth Observation Model for Many Resolutions, Scales, and Modalities
    "https://arxiv.org/abs/2412.14164",  # MetaMorph: Multimodal Understanding and Generation via Instruction Tuning
    "https://arxiv.org/abs/2412.14171",  # Thinking in Space: How Multimodal Large Language Models See, Remember, and Recall Spaces
    "https://arxiv.org/abs/2412.14640",  # Adaptive Prompt Tuning: Vision Guided Prompt Tuning with Cross-Attention for Fine-Grained Few-Shot Learning
    "https://arxiv.org/abs/2412.14803",  # Video Prediction Policy: A Generalist Robot Policy with Predictive Visual Representations
    "https://arxiv.org/abs/2412.14835",  # Progressive Multimodal Reasoning via Active Retrieval
    "https://arxiv.org/abs/2412.14957",  # Dream to Manipulate: Compositional World Models Empowering Robot Imitation Learning with Imagination
    "https://arxiv.org/abs/2412.15109",  # Predictive Inverse Dynamics Models are Scalable Learners for Robotic Manipulation
    "https://arxiv.org/abs/2412.15188",  # LMFusion: Adapting Pretrained Language Models for Multimodal Generation
    "https://arxiv.org/abs/2412.15214",  # LeviTor: 3D Trajectory Oriented Image-to-Video Synthesis
    "https://arxiv.org/abs/2412.16334",  # DINOv2 Meets Text: A Unified Framework for Image- and Pixel-Level Vision-Language Alignment
    "https://arxiv.org/abs/2412.17451",  # Diving into Self-Evolving Training for Multimodal Reasoning
    "https://arxiv.org/abs/2412.17730",  # Mimicking-Bench: A Benchmark for Generalizable Humanoid-Scene Interaction Learning via Human Mimicking
    "https://arxiv.org/abs/2412.17804",  # GausSim: Foreseeing Reality by Gaussian Simulator for Elastic Objects
    "https://arxiv.org/abs/2412.18072",  # MMFactory: A Universal Solution Search Engine for Vision-Language Tasks
    "https://arxiv.org/abs/2412.18090",  # Multi-Point Positional Insertion Tuning for Small Object Detection
    "https://arxiv.org/abs/2412.18194",  # VLABench: A Large-Scale Benchmark for Language-Conditioned Robotics Manipulation with Long-Horizon Reasoning Tasks
    "https://arxiv.org/abs/2412.18273",  # Sampling Bag of Views for Open-Vocabulary Object Detection
    "https://arxiv.org/abs/2412.18319",  # Mulberry: Empowering MLLM with o1-like Reasoning and Reflection via Collective Monte Carlo Tree Search
    "https://arxiv.org/abs/2412.18619",  # Next Token Prediction Towards Multimodal Intelligence: A Comprehensive Survey
    "https://arxiv.org/abs/2412.18781",  # Robustness Evaluation of Offline Reinforcement Learning for Robot Control Against Action Perturbations
    "https://arxiv.org/abs/2412.20404",  # Open-Sora: Democratizing Efficient Video Production for All
    "https://arxiv.org/abs/2501.00289",  # Dual Diffusion for Unified Image Generation and Understanding
    "https://arxiv.org/abs/2501.00663",  # Titans: Learning to Memorize at Test Time
    "https://arxiv.org/abs/2501.01478",  # Enhancing Reasoning through Process Supervision with Monte Carlo Tree Search
    "https://arxiv.org/abs/2501.01774",  # A Unifying View of Linear Function Approximation in Off-Policy RL Through Matrix Splitting and Preconditioning
    "https://arxiv.org/abs/2501.01830",  # Auto-RT: Automatic Jailbreak Strategy Exploration for Red-Teaming Large Language Models
    "https://arxiv.org/abs/2501.02189",  # A Survey of State of the Art Large Vision Language Models: Alignment, Benchmark, Evaluations and Challenges
    "https://arxiv.org/abs/2501.02765",  # Visual Large Language Models for Generalized and Specialized Applications
    "https://arxiv.org/abs/2501.03575",  # Cosmos World Foundation Model Platform for Physical AI
    "https://arxiv.org/abs/2501.04693",  # Beyond Sight: Finetuning Generalist Robot Policies with Heterogeneous Sensors via Language Grounding
    "https://arxiv.org/abs/2501.04823",  # Learning Robot Safety from Sparse Human Feedback using Conformal Prediction
    "https://arxiv.org/abs/2501.05366",  # Search-o1: Agentic Search-Enhanced Large Reasoning Models
    "https://arxiv.org/abs/2501.05452",  # ReFocus: Visual Editing as a Chain of Thought for Structured Image Understanding
    "https://arxiv.org/abs/2501.05803",  # Test-time Alignment of Diffusion Models without Reward Over-optimization
    "https://arxiv.org/abs/2501.06848",  # A General Framework for Inference-time Scaling and Steering of Diffusion Models
    "https://arxiv.org/abs/2501.07542",  # Imagine while Reasoning in Space: Multimodal Visualization-of-Thought
    "https://arxiv.org/abs/2501.08316",  # Diffusion Adversarial Post-Training for One-Step Video Generation
    "https://arxiv.org/abs/2501.08325",  # GameFactory: Creating New Games with Generative Interactive Videos
    "https://arxiv.org/abs/2501.09038",  # Do generative video models understand physical principles?
    "https://arxiv.org/abs/2501.09223",  # Foundations of Large Language Models
    "https://arxiv.org/abs/2501.09333",  # Prompt-CAM: Making Vision Transformers Interpretable for Fine-Grained Analysis
    "https://arxiv.org/abs/2501.09686",  # Towards Large Reasoning Models: A Survey of Reinforced Reasoning with Large Language Models
    "https://arxiv.org/abs/2501.09747",  # FAST: Efficient Action Tokenization for Vision-Language-Action Models
    "https://arxiv.org/abs/2501.10074",  # SpatialCoT: Advancing Spatial Reasoning through Coordinate Alignment and Chain-of-Thought for Embodied Task Planning
    "https://arxiv.org/abs/2501.10100",  # Robotic World Model: A Neural Network Simulator for Robust Policy Optimization in Robotics
    "https://arxiv.org/abs/2501.10395",  # Towards General Purpose Robots at Scale: Lifelong Learning and Learning to Use Memory
    "https://arxiv.org/abs/2501.10928",  # Generative Physical AI in Vision: A Survey
    "https://arxiv.org/abs/2501.11223",  # Reasoning Language Models: A Blueprint
    "https://arxiv.org/abs/2501.11858",  # EmbodiedEval: Evaluate Multimodal LLMs as Embodied Agents
    "https://arxiv.org/abs/2501.12202",  # Hunyuan3D 2.0: Scaling Diffusion Models for High Resolution Textured 3D Assets Generation
    "https://arxiv.org/abs/2501.13620",  # A Cognitive Paradigm Approach to Probe the Perception-Reasoning Interface in VLMs
    "https://arxiv.org/abs/2501.13787",  # Parameter-Efficient Fine-Tuning for Foundation Models
    "https://arxiv.org/abs/2501.13918",  # Improving Video Generation with Human Feedback
    "https://arxiv.org/abs/2501.13926",  # Can We Generate Images with CoT? Let's Verify and Reinforce Image Generation Step by Step
    "https://arxiv.org/abs/2501.14208",  # You Only Teach Once: Learn One-Shot Bimanual Robotic Manipulation from Video Demonstrations
    "https://arxiv.org/abs/2501.14622",  # ACT-JEPA: Novel Joint-Embedding Predictive Architecture for Efficient Policy Representation Learning
    "https://arxiv.org/abs/2501.15129",  # EvoRL: A GPU-accelerated Framework for Evolutionary Reinforcement Learning
    "https://arxiv.org/abs/2501.15228",  # Improving Retrieval-Augmented Generation through Multi-Agent Reinforcement Learning
    "https://arxiv.org/abs/2501.15830",  # SpatialVLA: Exploring Spatial Representations for Visual-Language-Action Model
    "https://arxiv.org/abs/2501.15910",  # The Sample Complexity of Online Reinforcement Learning: A Multi-model Perspective
    "https://arxiv.org/abs/2501.16389",  # Bridging the Sim2Real Gap: Vision Encoder Pre-Training for Visuomotor Policy Transfer
    "https://arxiv.org/abs/2501.16411",  # PhysBench: Benchmarking and Enhancing Vision-Language Models for Physical World Understanding
    "https://arxiv.org/abs/2501.16443",  # Object-Centric World Models from Few-Shot Annotations for Sample-Efficient Reinforcement Learning
    "https://arxiv.org/abs/2501.16550",  # PhysAnimator: Physics-Guided Generative Cartoon Animation
    "https://arxiv.org/abs/2501.16664",  # Improving Vision-Language-Action Model with Online Reinforcement Learning
    "https://arxiv.org/abs/2501.17161",  # SFT Memorizes, RL Generalizes: A Comparative Study of Foundation Model Post-training
    "https://arxiv.org/abs/2501.17811",  # Janus-Pro: Unified Multimodal Understanding and Generation with Data and Model Scaling
    "https://arxiv.org/abs/2501.18564",  # SAM2Act: Integrating Visual Foundation Model with A Memory Architecture for Robotic Manipulation
    "https://arxiv.org/abs/2501.18867",  # UP-VLA: A Unified Understanding and Prediction Model for Embodied Agent
    "https://arxiv.org/abs/2501.18954",  # LLMDet: Learning Strong Open-Vocabulary Object Detectors under the Supervision of Large Language Models
    "https://arxiv.org/abs/2501.18982",  # OmniPhysGS: 3D Constitutive Gaussians for General Physics-Based Dynamics Generation
    "https://arxiv.org/abs/2501.19201",  # Efficient Reasoning with Hidden Thinking
    "https://arxiv.org/abs/2501.19393",  # s1: Simple test-time scaling
    "https://arxiv.org/abs/2502.00466",  # EDELINE: Enhancing Memory in Diffusion-based World Models via Linear-Time Sequence Modeling
    "https://arxiv.org/abs/2502.00560",  # Solving Football by Exploiting Equilibrium Structure of 2p0s Differential Games with One-Sided Information
    "https://arxiv.org/abs/2502.00622",  # Inference-Time Enhancement of Generative Robot Policies via Predictive World Modeling
    "https://arxiv.org/abs/2502.00639",  # Half-order Fine-Tuning for Diffusion Model: A Recursive Likelihood Ratio Optimizer
    "https://arxiv.org/abs/2502.00814",  # Disentangling Length Bias In Preference Learning Via Response-Conditioned Modeling
    "https://arxiv.org/abs/2502.00935",  # Generalizing Safety Beyond Collision-Avoidance via Latent-Space Reachability Analysis
    "https://arxiv.org/abs/2502.01143",  # ASAP: Aligning Simulation and Real-World Physics for Learning Agile Humanoid Whole-Body Skills
    "https://arxiv.org/abs/2502.01203",  # KL-Regularized RLHF with Multiple Reference Models: Exact Solutions and Sample Complexity
    "https://arxiv.org/abs/2502.01384",  # Fine-Tuning Discrete Diffusion Models with Policy Gradient Methods
    "https://arxiv.org/abs/2502.01784",  # VILP: Imitation Learning with Latent Video Planning
    "https://arxiv.org/abs/2502.01828",  # From Foresight to Forethought: VLM-In-the-Loop Policy Steering via Latent Alignment
    "https://arxiv.org/abs/2502.01962",  # Memory Efficient Transformer Adapter for Dense Predictions
    "https://arxiv.org/abs/2502.02013",  # Layer by Layer: Uncovering Hidden Representations in Language Models
    "https://arxiv.org/abs/2502.02088",  # Dual-IPO: Dual-Iterative Preference Optimization for Text-to-Video Generation
    "https://arxiv.org/abs/2502.02133",  # Synthesis of Model Predictive Control and Reinforcement Learning: Survey and Classification
    "https://arxiv.org/abs/2502.02202",  # Multi-level Supervised Contrastive Learning
    "https://arxiv.org/abs/2502.02316",  # DIME:Diffusion-Based Maximum Entropy Reinforcement Learning
    "https://arxiv.org/abs/2502.02339",  # AStar: Boosting Multimodal Reasoning with Automated Structured Thinking
    "https://arxiv.org/abs/2502.02492",  # VideoJAM: Joint Appearance-Motion Representations for Enhanced Motion Generation in Video Models
    "https://arxiv.org/abs/2502.02869",  # Towards Large-Scale In-Context Reinforcement Learning by Meta-Training in Randomized Worlds
    "https://arxiv.org/abs/2502.03214",  # iVISPAR -- An Interactive Visual-Spatial Reasoning Benchmark for VLMs
    "https://arxiv.org/abs/2502.03275",  # Token Assorted: Mixing Latent and Text Tokens for Improved Language Model Reasoning
    "https://arxiv.org/abs/2502.03387",  # LIMO: Less is More for Reasoning
    "https://arxiv.org/abs/2502.03550",  # TD-M(PC)$^2$: Improving Temporal Difference MPC Through Policy Constraint
    "https://arxiv.org/abs/2502.03639",  # Towards Physical Understanding in Video Generation: A 3D Point Regularization Approach
    "https://arxiv.org/abs/2502.03714",  # Universal Sparse Autoencoders: Interpretable Cross-Model Concept Alignment
    "https://arxiv.org/abs/2502.03752",  # Self-Improving Skill Learning for Robust Skill-based Meta-Reinforcement Learning
    "https://arxiv.org/abs/2502.04144",  # HD-EPIC: A Highly-Detailed Egocentric Video Dataset
    "https://arxiv.org/abs/2502.04463",  # Training Language Models to Reason Efficiently
    "https://arxiv.org/abs/2502.04873",  # Training-free Task-oriented Grasp Generation
    "https://arxiv.org/abs/2502.04979",  # Prompt Tuning Decision Transformers with Structured and Scalable Bandits
    "https://arxiv.org/abs/2502.05086",  # REASSEMBLE: A Multimodal Dataset for Contact-rich Robotic Assembly and Disassembly
    "https://arxiv.org/abs/2502.05171",  # Scaling up Test-Time Compute with Latent Reasoning: A Recurrent Depth Approach
    "https://arxiv.org/abs/2502.05206",  # Safety at Scale: A Comprehensive Survey of Large Model and Agent Safety
    "https://arxiv.org/abs/2502.05234",  # Optimizing Temperature for Language Models with Multi-Sample Inference
    "https://arxiv.org/abs/2502.05450",  # ConRFT: A Reinforced Fine-tuning Method for VLA Models via Consistency Policy
    "https://arxiv.org/abs/2502.05454",  # Temporal Representation Alignment: Successor Features Enable Emergent Compositionality in Robot Instruction Following
    "https://arxiv.org/abs/2502.05503",  # A Physical Coherence Benchmark for Evaluating Video Generation Models via Optical Flow-guided Frame Prediction
    "https://arxiv.org/abs/2502.05726",  # Improving Environment Novelty Quantification for Effective Unsupervised Environment Design
    "https://arxiv.org/abs/2502.05907",  # EvoAgent: Self-evolving Agent with Continual World Model for Long-Horizon Tasks
    "https://arxiv.org/abs/2502.06051",  # Towards a Sharp Analysis of Offline Policy Learning for $f$-Divergence-Regularized Contextual Bandits
    "https://arxiv.org/abs/2502.06233",  # Confidence Improves Self-Consistency in LLMs
    "https://arxiv.org/abs/2502.06309",  # Analog In-memory Training on General Non-ideal Resistive Elements: The Impact of Response Functions
    "https://arxiv.org/abs/2502.06575",  # Predictive Red Teaming: Breaking Policies Without Breaking Robots
    "https://arxiv.org/abs/2502.06772",  # ReasonFlux: Hierarchical LLM Reasoning via Scaling Thought Templates
    "https://arxiv.org/abs/2502.07007",  # Grounding Creativity in Physics: A Brief Survey of Physical Priors in AIGC
    "https://arxiv.org/abs/2502.07193",  # Provably Efficient Online RLHF with One-Pass Reward Modeling
    "https://arxiv.org/abs/2502.07266",  # When More is Less: Understanding Chain-of-Thought Length in LLMs
    "https://arxiv.org/abs/2502.07279",  # Exploratory Diffusion Model for Unsupervised Reinforcement Learning
    "https://arxiv.org/abs/2502.07408",  # Maximal Brain Damage Without Data or Optimization: Disrupting Neural Networks via Sign-Bit Flips
    "https://arxiv.org/abs/2502.07503",  # Recursive Inference Scaling: A Winning Path to Scalable Inference in Language and Multimodal Systems
    "https://arxiv.org/abs/2502.07523",  # Scaling Off-Policy Reinforcement Learning with Batch and Weight Normalization
    "https://arxiv.org/abs/2502.08021",  # Model Selection for Off-policy Evaluation: New Algorithms and Experimental Protocol
    "https://arxiv.org/abs/2502.08378",  # Learning Humanoid Standing-up Control across Diverse Postures
    "https://arxiv.org/abs/2502.08643",  # A Real-to-Sim-to-Real Approach to Robotic Manipulation with VLM-Generated Iterative Keypoint Rewards
    "https://arxiv.org/abs/2502.08645",  # Re$^3$Sim: Generating High-Fidelity Simulation Data via 3D-Photorealistic Real-to-Sim for Robotic Manipulation
    "https://arxiv.org/abs/2502.08844",  # MuJoCo Playground
    "https://arxiv.org/abs/2502.08922",  # Self-Consistency of the Internal Reward Models Improves Self-Rewarding Language Models
    "https://arxiv.org/abs/2502.08938",  # Reevaluating Policy Gradient Methods for Imperfect-Information Games
    "https://arxiv.org/abs/2502.09324",  # Depth-Bounds for Neural Networks via the Braid Arrangement
    "https://arxiv.org/abs/2502.09560",  # EmbodiedBench: Comprehensive Benchmarking Multi-modal Large Language Models for Vision-Driven Embodied Agents
    "https://arxiv.org/abs/2502.09992",  # Large Language Diffusion Models
    "https://arxiv.org/abs/2502.10028",  # 3D Dynamics-Aware Manipulation: Endowing Manipulation Policies with 3D Foresight
    "https://arxiv.org/abs/2502.10040",  # Diffusion Trajectory-guided Policy for Long-horizon Robot Manipulation
    "https://arxiv.org/abs/2502.10138",  # Provably Efficient RL under Episode-Wise Safety in Constrained MDPs with Linear Function Approximation
    "https://arxiv.org/abs/2502.10363",  # BeamDojo: Learning Agile Humanoid Locomotion on Sparse Footholds
    "https://arxiv.org/abs/2502.10385",  # Simplifying DINO via Coding Rate Regularization
    "https://arxiv.org/abs/2502.10550",  # Memory, Benchmark & Robots: A Benchmark for Solving Complex Tasks with Reinforcement Learning
    "https://arxiv.org/abs/2502.10694",  # Simulations of Common Unsupervised Domain Adaptation Algorithms for Image Classification
    "https://arxiv.org/abs/2502.10862",  # Accelerated co-design of robots through morphological pretraining
    "https://arxiv.org/abs/2502.10894",  # Bridging the Sim-to-Real Gap for Athletic Loco-Manipulation
    "https://arxiv.org/abs/2502.10983",  # Learning Quiet Walking for a Small Home Robot
    "https://arxiv.org/abs/2502.11377",  # PrivilegedDreamer: Explicit Imagination of Privileged Information for Rapid Adaptation of Learned Policies
    "https://arxiv.org/abs/2502.11859",  # Defining and Evaluating Visual Language Models' Basic Spatial Abilities: A Perspective from Psychometrics
    "https://arxiv.org/abs/2502.12152",  # Learning Getting-Up Policies for Real-World Humanoid Robots
    "https://arxiv.org/abs/2502.12191",  # AnyTouch: Learning Unified Static-Dynamic Representation across Multiple Visuo-tactile Sensors
    "https://arxiv.org/abs/2502.12530",  # Translate Policy to Language: Flow Matching Generated Rewards for LLM Explanations
    "https://arxiv.org/abs/2502.13130",  # Magma: A Foundation Model for Multimodal AI Agents
    "https://arxiv.org/abs/2502.13143",  # SoFar: Language-Grounded Orientation Bridges Spatial Reasoning and Object Manipulation
    "https://arxiv.org/abs/2502.13144",  # RAD: Training an End-to-End Driving Policy via Large-Scale 3DGS-based Reinforcement Learning
    "https://arxiv.org/abs/2502.14010",  # Which Attention Heads Matter for In-Context Learning?
    "https://arxiv.org/abs/2502.14172",  # A Finite Sample Analysis of Distributional TD Learning with Linear Function Approximation
    "https://arxiv.org/abs/2502.14214",  # Asymmetric Co-Training for Source-Free Few-Shot Domain Adaptation
    "https://arxiv.org/abs/2502.14420",  # ChatVLA: Unified Multimodal Understanding and Robot Control with Vision-Language-Action Model
    "https://arxiv.org/abs/2502.14457",  # Watch Less, Feel More: Sim-to-Real RL for Generalizable Articulated Object Manipulation via Motion Adaptation and Impedance Control
    "https://arxiv.org/abs/2502.14786",  # SigLIP 2: Multilingual Vision-Language Encoders with Improved Semantic Understanding, Localization, and Dense Features
    "https://arxiv.org/abs/2502.14795",  # Humanoid-VLA: Towards Universal Humanoid Control with Visual Integration
    "https://arxiv.org/abs/2502.14819",  # Learning from Reward-Free Offline Data: A Case for Planning with Latent Dynamics Models
    "https://arxiv.org/abs/2502.15280",  # Hyperspherical Normalization for Scalable Deep Reinforcement Learning
    "https://arxiv.org/abs/2502.15798",  # MaxSup: Overcoming Representation Collapse in Label Smoothing
    "https://arxiv.org/abs/2502.15922",  # On the Design of Safe Continual RL Methods for Control of Nonlinear Systems
    "https://arxiv.org/abs/2502.16025",  # FeatSharp: Your Vision Model Features, Sharper
    "https://arxiv.org/abs/2502.16420",  # AnyDexGrasp: General Dexterous Grasping for Different Hands with Human-level Learning Efficiency
    "https://arxiv.org/abs/2502.16435",  # Human Cognitive Benchmarks Reveal Foundational Visual Gaps in MLLMs
    "https://arxiv.org/abs/2502.16707",  # Reflective Planning: Vision-Language Models for Multi-Stage Long-Horizon Robotic Manipulation
    "https://arxiv.org/abs/2502.16736",  # Adaptive Conformal Guidance for Learning under Uncertainty
    "https://arxiv.org/abs/2502.16816",  # Finite-Sample Analysis of Policy Evaluation for Robust Average Reward Reinforcement Learning
    "https://arxiv.org/abs/2502.16852",  # Improving LLM General Preference Alignment via Optimistic Online Mirror Descent
    "https://arxiv.org/abs/2502.16944",  # Pretrain Value, Not Reward: Decoupled Value Policy Optimization
    "https://arxiv.org/abs/2502.16982",  # Muon is Scalable for LLM Training
    "https://arxiv.org/abs/2502.17159",  # RobustMerge: Parameter-Efficient Model Merging for MLLMs with Direction Robustness
    "https://arxiv.org/abs/2502.17322",  # TDMPBC: Self-Imitative Reinforcement Learning for Humanoid Robot Control
    "https://arxiv.org/abs/2502.17416",  # Reasoning with Latent Thoughts: On the Power of Looped Transformers
    "https://arxiv.org/abs/2502.17422",  # MLLMs Know Where to Look: Training-free Perception of Small Visual Details with Multimodal LLMs
    "https://arxiv.org/abs/2502.17425",  # Introducing Visual Perception Token into Multimodal Large Language Model
    "https://arxiv.org/abs/2502.17666",  # Yes, Q-learning Helps Offline In-Context RL
    "https://arxiv.org/abs/2502.19544",  # Efficient Reinforcement Learning by Guiding Generalist World Models with Non-Curated Data
    "https://arxiv.org/abs/2502.19638",  # Sensor-Invariant Tactile Representation
    "https://arxiv.org/abs/2502.19645",  # Fine-Tuning Vision-Language-Action Models: Optimizing Speed and Success
    "https://arxiv.org/abs/2502.19868",  # C-Drag: Chain-of-Thought Driven Motion Controller for Video Generation
    "https://arxiv.org/abs/2502.20061",  # HiFAR: Multi-Stage Curriculum Learning for High-Dynamics Humanoid Fall Recovery
    "https://arxiv.org/abs/2502.20120",  # Rethinking Multimodal Learning from the Perspective of Mitigating Classification Ability Disproportion
    "https://arxiv.org/abs/2502.20396",  # Sim-to-Real Reinforcement Learning for Vision-Based Dexterous Manipulation on Humanoids
    "https://arxiv.org/abs/2502.20548",  # $Q\sharp$: Provably Optimal Distributional RL for LLM Post-Training
    "https://arxiv.org/abs/2502.20694",  # WorldModelBench: Judging Video Generation Models As World Models
    "https://arxiv.org/abs/2502.20946",  # Generative Uncertainty in Diffusion Models
    "https://arxiv.org/abs/2502.21074",  # CODI: Compressing Chain-of-Thought into Continuous Space via Self-Distillation
    "https://arxiv.org/abs/2502.21269",  # Dynamical Decoupling of Generalization and Overfitting in Large Two-Layer Networks
    "https://arxiv.org/abs/2502.21321",  # LLM Post-Training: A Deep Dive into Reasoning Large Language Models
    "https://arxiv.org/abs/2503.00200",  # Unified Video Action Model
    "https://arxiv.org/abs/2503.00641",  # How to Probe: Simple Yet Effective Techniques for Improving Post-hoc Explanations
    "https://arxiv.org/abs/2503.00692",  # Learning Perceptive Humanoid Locomotion over Challenging Terrain
    "https://arxiv.org/abs/2503.00743",  # Quality-Driven Curation of Remote Sensing Vision-Language Data via Learned Scoring Models
    "https://arxiv.org/abs/2503.00761",  # TRACE: A Self-Improving Framework for Robot Behavior Forecasting with Vision-Language Models
    "https://arxiv.org/abs/2503.00923",  # HWC-Loco: A Hierarchical Whole-Body Control Approach to Robust Humanoid Locomotion
    "https://arxiv.org/abs/2503.01058",  # Training Tactile Sensors to Learn Force Sensing from Each Other
    "https://arxiv.org/abs/2503.01067",  # All Roads Lead to Likelihood: The Value of Reinforcement Learning in Fine-Tuning
    "https://arxiv.org/abs/2503.01584",  # SENSEI: Semantic Exploration Guided by Foundation Models to Learn Versatile World Models
    "https://arxiv.org/abs/2503.01619",  # Advancing vision-language models in front-end development via data synthesis
    "https://arxiv.org/abs/2503.01773",  # Why Is Spatial Reasoning Hard for VLMs? An Attention Mechanism Perspective on Focus Areas
    "https://arxiv.org/abs/2503.01776",  # Beyond Matryoshka: Revisiting Sparse Coding for Adaptive Representation
    "https://arxiv.org/abs/2503.01785",  # Visual-RFT: Visual Reinforcement Fine-Tuning
    "https://arxiv.org/abs/2503.01842",  # Discrete-Time Hybrid Automata Learning: Legged Locomotion Meets Skateboarding
    "https://arxiv.org/abs/2503.02039",  # Dynamic Search for Inference-Time Alignment in Diffusion Models
    "https://arxiv.org/abs/2503.02269",  # Experience Replay with Random Reshuffling
    "https://arxiv.org/abs/2503.02310",  # PD-VLA: Accelerating Vision-Language-Action Model Integrated with Action Chunking via Parallel Decoding
    "https://arxiv.org/abs/2503.02623",  # Rewarding Doubt: A Reinforcement Learning Approach to Calibrated Confidence Expression of Large Language Models
    "https://arxiv.org/abs/2503.02881",  # Reactive Diffusion Policy: Slow-Fast Visual-Tactile Policy Learning for Contact-Rich Manipulation
    "https://arxiv.org/abs/2503.03480",  # SafeVLA: Towards Safety Alignment of Vision-Language-Action Model via Constrained Learning
    "https://arxiv.org/abs/2503.03660",  # Chunking the Critic: A Transformer-based Soft Actor-Critic with N-Step Returns
    "https://arxiv.org/abs/2503.03746",  # Process-based Self-Rewarding Language Models
    "https://arxiv.org/abs/2503.04412",  # Wider or Deeper? Scaling LLM Inference-Time Compute with Adaptive Branching Tree Search
    "https://arxiv.org/abs/2503.04641",  # Simulating the Real World: A Unified Survey of Multimodal Generative Models
    "https://arxiv.org/abs/2503.04720",  # FluidNexus: 3D Fluid Reconstruction and Prediction from a Single Video
    "https://arxiv.org/abs/2503.05035",  # QuietPaw: Learning Quadrupedal Locomotion with Versatile Noise Preference Alignment
    "https://arxiv.org/abs/2503.05255",  # CMMCoT: Enhancing Complex Multi-Image Comprehension via Multi-Modal Chain-of-Thought and Memory Augmentation
    "https://arxiv.org/abs/2503.05592",  # R1-Searcher: Incentivizing the Search Capability in LLMs via Reinforcement Learning
    "https://arxiv.org/abs/2503.05652",  # BEHAVIOR Robot Suite: Streamlining Real-World Whole-Body Manipulation for Everyday Household Activities
    "https://arxiv.org/abs/2503.05696",  # A Multi-Fidelity Control Variate Approach for Policy Gradient Estimation
    "https://arxiv.org/abs/2503.06063",  # Multi-Layer Visual Feature Fusion in Multimodal LLMs: Methods, Analysis, and Best Practices
    "https://arxiv.org/abs/2503.06132",  # USP: Unified Self-Supervised Pretraining for Image Generation and Understanding
    "https://arxiv.org/abs/2503.06380",  # TI-JEPA: An Innovative Energy-based Joint Embedding Strategy for Text-Image Multimodal Systems
    "https://arxiv.org/abs/2503.06520",  # Seg-Zero: Reasoning-Chain Guided Segmentation via Cognitive Reinforcement
    "https://arxiv.org/abs/2503.06626",  # DiffCLIP: Differential Attention Meets CLIP
    "https://arxiv.org/abs/2503.06669",  # AgiBot World Colosseo: A Large-scale Manipulation Platform for Scalable and Intelligent Embodied Systems
    "https://arxiv.org/abs/2503.06736",  # Safe, Task-Consistent Manipulation with Operational Space Control Barrier Functions
    "https://arxiv.org/abs/2503.06749",  # Vision-R1: Incentivizing Reasoning Capability in Multimodal Large Language Models
    "https://arxiv.org/abs/2503.06800",  # VideoPhy-2: A Challenging Action-Centric Physical Commonsense Evaluation in Video Generation
    "https://arxiv.org/abs/2503.07360",  # AffordDexGrasp: Open-set Language-guided Dexterous Grasp with Generalizable-Instructive Affordance
    "https://arxiv.org/abs/2503.07365",  # MM-Eureka: Exploring the Frontiers of Multimodal Reasoning with Rule-based Reinforcement Learning
    "https://arxiv.org/abs/2503.07511",  # PointVLA: Injecting the 3D World into Vision-Language-Action Models
    "https://arxiv.org/abs/2503.07523",  # VisRL: Intention-Driven Visual Perception via Reinforced Reasoning
    "https://arxiv.org/abs/2503.07572",  # Optimizing Test-Time Compute via Meta Reinforcement Fine-Tuning
    "https://arxiv.org/abs/2503.07926",  # Learning Gentle Grasping Using Vision, Sound, and Touch
    "https://arxiv.org/abs/2503.08153",  # WISA: World Simulator Assistant for Physics-Aware Text-to-Video Generation
    "https://arxiv.org/abs/2503.08497",  # MMRL: Multi-Modal Representation Learning for Vision-Language Models
    "https://arxiv.org/abs/2503.08548",  # TLA: Tactile-Language-Action Model for Contact-Rich Manipulation
    "https://arxiv.org/abs/2503.08558",  # Can We Detect Failures Without Failure Data? Uncertainty-Aware Runtime Failure Detection for Imitation Learning Policies
    "https://arxiv.org/abs/2503.08998",  # From Task-Specific Models to Unified Systems: A Review of Model Merging Approaches
    "https://arxiv.org/abs/2503.09186",  # Rethinking Bimanual Robotic Manipulation: Learning with Decoupled Interaction Framework
    "https://arxiv.org/abs/2503.09501",  # ReMA: Learning to Meta-think for LLMs with Multi-Agent Reinforcement Learning
    "https://arxiv.org/abs/2503.09516",  # Search-R1: Training LLMs to Reason and Leverage Search Engines with Reinforcement Learning
    "https://arxiv.org/abs/2503.09527",  # CombatVLA: An Efficient Vision-Language-Action Model for Combat Tasks in 3D Action Role-Playing Games
    "https://arxiv.org/abs/2503.09561",  # Strategyproof Reinforcement Learning from Human Feedback
    "https://arxiv.org/abs/2503.09567",  # Towards Reasoning Era: A Survey of Long Chain-of-Thought for Reasoning Large Language Models
    "https://arxiv.org/abs/2503.09595",  # PISA Experiments: Exploring Physics Post-Training for Video Diffusion Models by Watching Stuff Drop
    "https://arxiv.org/abs/2503.09867",  # Oh-A-DINO: Understanding and Enhancing Attribute-Level Information in Self-Supervised Object-Centric Representations
    "https://arxiv.org/abs/2503.10118",  # An Real-Sim-Real (RSR) Loop Framework for Generalizable Robotic Policy Transfer with Differentiable Simulation
    "https://arxiv.org/abs/2503.10291",  # VisualPRM: An Effective Process Reward Model for Multimodal Reasoning
    "https://arxiv.org/abs/2503.10460",  # Light-R1: Curriculum SFT, DPO and RL for Long COT from Scratch and Beyond
    "https://arxiv.org/abs/2503.10622",  # Transformers without Normalization
    "https://arxiv.org/abs/2503.10626",  # NIL: No-data Imitation Learning by Leveraging Pre-trained Video Diffusion Models
    "https://arxiv.org/abs/2503.10631",  # HybridVLA: Collaborative Diffusion and Autoregression in a Unified Vision-Language-Action Model
    "https://arxiv.org/abs/2503.10639",  # GoT: Unleashing Reasoning Capability of Multimodal Large Language Model for Visual Generation and Editing
    "https://arxiv.org/abs/2503.10705",  # Enhanced Continual Learning of Vision-Language Models with Model Fusion
    "https://arxiv.org/abs/2503.10949",  # Safe Continual Domain Adaptation after Sim2Real Transfer of Reinforcement Learning Policies in Robotics
    "https://arxiv.org/abs/2503.11089",  # EmbodiedVSR: Dynamic Scene Graph-Guided Chain-of-Thought Reasoning for Visual Spatial Tasks
    "https://arxiv.org/abs/2503.11117",  # Beyond the Destination: A Novel Benchmark for Exploration-Aware Embodied Question Answering
    "https://arxiv.org/abs/2503.11339",  # Contextual Similarity Distillation: Ensemble Uncertainties with a Single Model
    "https://arxiv.org/abs/2503.11739",  # CoLLMLight: Cooperative Large Language Model Agents for Network-Wide Traffic Signal Control
    "https://arxiv.org/abs/2503.12605",  # Multimodal Chain-of-Thought Reasoning: A Comprehensive Survey
    "https://arxiv.org/abs/2503.12797",  # DeepPerception: Advancing R1-like Cognitive Visual Perception in MLLMs for Knowledge-Intensive Visual Grounding
    "https://arxiv.org/abs/2503.12799",  # Grounded Chain-of-Thought for Multimodal Large Language Models
    "https://arxiv.org/abs/2503.12811",  # A Multi-Power Law for Loss Curve Prediction Across Learning Rate Schedules
    "https://arxiv.org/abs/2503.13111",  # MM-Spatial: Exploring 3D Spatial Understanding in Multimodal LLMs
    "https://arxiv.org/abs/2503.13436",  # Unified Autoregressive Visual Generation and Understanding with Continuous Tokens
    "https://arxiv.org/abs/2503.13441",  # Humanoid Policy ~ Human Policy
    "https://arxiv.org/abs/2503.13446",  # MoManipVLA: Transferring Vision-language-action Models for General Mobile Manipulation
    "https://arxiv.org/abs/2503.13551",  # Towards Hierarchical Multi-Step Reward Models for Enhanced Reasoning in Large Language Models
    "https://arxiv.org/abs/2503.13916",  # Learning Bimanual Manipulation via Action Chunking and Inter-Arm Coordination with Transformers
    "https://arxiv.org/abs/2503.14378",  # Impossible Videos
    "https://arxiv.org/abs/2503.14476",  # DAPO: An Open-Source LLM Reinforcement Learning System at Scale
    "https://arxiv.org/abs/2503.14485",  # Lux Post Facto: Learning Portrait Performance Relighting with Conditional Video Diffusion and a Hybrid Dataset
    "https://arxiv.org/abs/2503.14489",  # Stable Virtual Camera: Generative View Synthesis with Diffusion Models
    "https://arxiv.org/abs/2503.14576",  # SocialJax: An Evaluation Suite for Multi-agent Reinforcement Learning in Sequential Social Dilemmas
    "https://arxiv.org/abs/2503.14734",  # GR00T N1: An Open Foundation Model for Generalist Humanoid Robots
    "https://arxiv.org/abs/2503.14833",  # Curiosity-Diffuser: Curiosity Guide Diffusion Models for Reliability
    "https://arxiv.org/abs/2503.14858",  # 1000 Layer Networks for Self-Supervised RL: Scaling Depth Can Enable New Goal-Reaching Capabilities
    "https://arxiv.org/abs/2503.15202",  # A Unified Framework for Real-Time Failure Handling in Robotics Using Vision-Language Models, Reactive Planner and Behavior Trees
    "https://arxiv.org/abs/2503.15386",  # CCDP: Composition of Conditional Diffusion Policies with Guided Sampling
    "https://arxiv.org/abs/2503.15477",  # What Makes a Reward Model a Good Teacher? An Optimization Perspective
    "https://arxiv.org/abs/2503.15485",  # TULIP: Towards Unified Language-Image Pretraining
    "https://arxiv.org/abs/2503.15558",  # Cosmos-Reason1: From Physical Common Sense To Embodied Reasoning
    "https://arxiv.org/abs/2503.15621",  # LLaVA-MORE: A Comparative Study of LLMs and Visual Backbones for Enhanced Visual Instruction Tuning
    "https://arxiv.org/abs/2503.16188",  # Think or Not Think: A Study of Explicit Thinking in Rule-Based Visual Reinforcement Fine-Tuning
    "https://arxiv.org/abs/2503.16219",  # Reinforcement Learning for Reasoning in Small LLMs: What Works and What Doesn't
    "https://arxiv.org/abs/2503.16394",  # Do Visual Imaginations Improve Vision-and-Language Navigation Agents?
    "https://arxiv.org/abs/2503.16416",  # Survey on Evaluation of LLM-based Agents
    "https://arxiv.org/abs/2503.16419",  # Stop Overthinking: A Survey on Efficient Reasoning for Large Language Models
    "https://arxiv.org/abs/2503.16434",  # Interactive Sketchpad: A Multimodal Tutoring System for Collaborative, Visual Problem-Solving
    "https://arxiv.org/abs/2503.16660",  # When Less is Enough: Adaptive Token Reduction for Efficient Image Representation
    "https://arxiv.org/abs/2503.16806",  # DyWA: Dynamics-adaptive World Action Model for Generalizable Non-prehensile Manipulation
    "https://arxiv.org/abs/2503.17338",  # Capturing Individual Human Preferences with Reward Features
    "https://arxiv.org/abs/2503.17352",  # OpenVLThinker: Complex Vision-Language Reasoning via Iterative SFT-RL Cycles
    "https://arxiv.org/abs/2503.17973",  # PhysTwin: Physics-Informed Reconstruction and Simulation of Deformable Objects from Videos
    "https://arxiv.org/abs/2503.18349",  # Human-Object Interaction via Automatically Designed VLM-Guided Motion Policy
    "https://arxiv.org/abs/2503.18470",  # MetaSpatial: Reinforcing 3D Spatial Reasoning in VLMs for the Metaverse
    "https://arxiv.org/abs/2503.18684",  # Efficient Continual Adaptation of Pretrained Robotic Policy with Online Meta-Learned Adapters
    "https://arxiv.org/abs/2503.18866",  # Reasoning to Learn from Latent Thoughts
    "https://arxiv.org/abs/2503.18929",  # Trajectory Balance with Asynchrony: Decoupling Exploration and Learning for Fast, Scalable LLM Post-Training
    "https://arxiv.org/abs/2503.18938",  # AdaWorld: Learning Adaptable World Models with Latent Actions
    "https://arxiv.org/abs/2503.18942",  # Video-T1: Test-Time Scaling for Video Generation
    "https://arxiv.org/abs/2503.18945",  # Aether: Geometric-Aware Unified World Modeling
    "https://arxiv.org/abs/2503.18991",  # Inverse Reinforcement Learning with Dynamic Reward Scaling for LLM Alignment
    "https://arxiv.org/abs/2503.19108",  # Your ViT is Secretly an Image Segmentation Model
    "https://arxiv.org/abs/2503.19263",  # DWIM: Towards Tool-aware Visual Reasoning via Discrepancy-aware Workflow Generation & Instruct-Masking Tuning
    "https://arxiv.org/abs/2503.19355",  # ST-VLM: Kinematic Instruction Tuning for Spatio-Temporal Reasoning in Vision-Language Models
    "https://arxiv.org/abs/2503.19457",  # G-DexGrasp: Generalizable Dexterous Grasping Synthesis Via Part-Aware Prior Retrieval and Prior-Assisted Generation
    "https://arxiv.org/abs/2503.19470",  # ReSearch: Learning to Reason with Search for LLMs via Reinforcement Learning
    "https://arxiv.org/abs/2503.19612",  # RL-finetuning LLMs from on- and off-policy data with a single algorithm
    "https://arxiv.org/abs/2503.19707",  # Mind the Gap: Benchmarking Spatial Reasoning in Vision-Language Models
    "https://arxiv.org/abs/2503.19757",  # Dita: Scaling Diffusion Transformer for Generalist Vision-Language-Action Policy
    "https://arxiv.org/abs/2503.19903",  # Scaling Vision Pre-Training to 4K Resolution
    "https://arxiv.org/abs/2503.20020",  # Gemini Robotics: Bringing AI into the Physical World
    "https://arxiv.org/abs/2503.20314",  # Wan: Open and Advanced Large-Scale Video Generative Models
    "https://arxiv.org/abs/2503.20654",  # AccidentSim: Generating Vehicle Collision Videos with Physically Realistic Collision Trajectories from Real-World Accident Reports
    "https://arxiv.org/abs/2503.20680",  # Vision as LoRA
    "https://arxiv.org/abs/2503.20746",  # PhysGen3D: Crafting a Miniature Interactive World from a Single Image
    "https://arxiv.org/abs/2503.20752",  # Reason-RFT: Reinforcement Fine-Tuning for Visual Reasoning of Vision Language Models
    "https://arxiv.org/abs/2503.20783",  # Understanding R1-Zero-Like Training: A Critical Perspective
    "https://arxiv.org/abs/2503.20822",  # Synthetic Video Enhances Physical Fidelity in Video Synthesis
    "https://arxiv.org/abs/2503.21047",  # World Model Agents with Change-Based Intrinsic Motivation
    "https://arxiv.org/abs/2503.21442",  # RainyGS: Efficient Rain Synthesis with Physically-Based Gaussian Splatting
    "https://arxiv.org/abs/2503.21614",  # A Survey of Efficient Reasoning for Large Reasoning Models: Language, Multimodality, and Beyond
    "https://arxiv.org/abs/2503.21668",  # Cognitive Science-Inspired Evaluation of Core Capabilities for Object Understanding in AI
    "https://arxiv.org/abs/2503.21745",  # 3DGen-Bench: Comprehensive Benchmark Suite for 3D Generative Models
    "https://arxiv.org/abs/2503.21755",  # VBench-2.0: Advancing Video Generation Benchmark Suite for Intrinsic Faithfulness
    "https://arxiv.org/abs/2503.21765",  # Exploring the Evolution of Physics Cognition in Video Generation: A Survey
    "https://arxiv.org/abs/2503.21776",  # Video-R1: Reinforcing Video Reasoning in MLLMs
    "https://arxiv.org/abs/2503.21983",  # Learning to Lie: Reinforcement Learning Attacks Damage Human-AI Teams and Teams of LLMs
    "https://arxiv.org/abs/2503.22020",  # CoT-VLA: Visual Chain-of-Thought Reasoning for Vision-Language-Action Models
    "https://arxiv.org/abs/2503.22122",  # REMAC: Self-Reflective and Self-Evolving Multi-Agent Collaboration for Long-Horizon Robot Manipulation
    "https://arxiv.org/abs/2503.22230",  # Exploring Data Scaling Trends and Effects in Reinforcement Learning from Human Feedback
    "https://arxiv.org/abs/2503.22976",  # From Flatland to Space: Teaching Vision-Language Models to Perceive and Reason in 3D
    "https://arxiv.org/abs/2503.23037",  # Agentic Large Language Models, a survey
    "https://arxiv.org/abs/2503.23077",  # Efficient Inference for Large Reasoning Models: A Survey
    "https://arxiv.org/abs/2503.23271",  # Learning Coordinated Bimanual Manipulation Policies using State Diffusion and Inverse Dynamics Models
    "https://arxiv.org/abs/2503.23368",  # VLIPP: Towards Physically Plausible Video Generation with Vision and Language Informed Physical Prior
    "https://arxiv.org/abs/2503.23383",  # ToRL: Scaling Tool-Integrated RL
    "https://arxiv.org/abs/2503.23508",  # Re-Aligning Language to Visual Objects with an Agentic Workflow
    "https://arxiv.org/abs/2503.23631",  # Intrinsically-Motivated Humans and Agents in Open-World Exploration
    "https://arxiv.org/abs/2503.23715",  # HOIGen-1M: A Large-scale Dataset for Human-Object Interaction Video Generation
    "https://arxiv.org/abs/2503.23765",  # STI-Bench: Are MLLMs Ready for Precise Spatial-Temporal World Understanding?
    "https://arxiv.org/abs/2503.23829",  # Crossing the Reward Bridge: Expanding RL with Verifiable Rewards Across Diverse Domains
    "https://arxiv.org/abs/2503.24067",  # TransMamba: A Sequence-Level Hybrid Transformer-Mamba Language Model
    "https://arxiv.org/abs/2503.24235",  # A Survey on Test-Time Scaling in Large Language Models: What, How, Where, and How Well?
    "https://arxiv.org/abs/2503.24278",  # AutoEval: Autonomous Evaluation of Generalist Robot Manipulation Policies in the Real World
    "https://arxiv.org/abs/2503.24290",  # Open-Reasoner-Zero: An Open Source Approach to Scaling Up Reinforcement Learning on the Base Model
    "https://arxiv.org/abs/2503.24361",  # Sim-and-Real Co-Training: A Simple Recipe for Vision-Based Robotic Manipulation
    "https://arxiv.org/abs/2503.24379",  # Any2Caption:Interpreting Any Condition to Caption for Controllable Video Generation
    "https://arxiv.org/abs/2504.00342",  # Aligning Diffusion Model with Problem Constraints for Trajectory Optimization
    "https://arxiv.org/abs/2504.00557",  # Efficient LLaMA-3.2-Vision by Trimming Cross-attended Visual Features
    "https://arxiv.org/abs/2504.00595",  # Open-Qwen2VL: Compute-Efficient Pre-Training of Fully-Open Multimodal LLMs on Academic Resources
    "https://arxiv.org/abs/2504.00883",  # Improved Visual-Spatial Reasoning via R1-Zero-Like Training
    "https://arxiv.org/abs/2504.00983",  # WorldScore: A Unified Evaluation Benchmark for World Generation
    "https://arxiv.org/abs/2504.01017",  # Scaling Language-Free Visual Representation Learning
    "https://arxiv.org/abs/2504.01204",  # Articulated Kinematics Distillation from Video Diffusion Models
    "https://arxiv.org/abs/2504.01538",  # AI-Newton: A Concept-Driven Physical Law Discovery System without Prior Physical Knowledge
    "https://arxiv.org/abs/2504.01805",  # SpaceR: Reinforcing MLLMs in Video Spatial Reasoning
    "https://arxiv.org/abs/2504.01990",  # Advances and Challenges in Foundation Agents: From Brain-Inspired Intelligence to Evolutionary, Collaborative, and Safe Systems
    "https://arxiv.org/abs/2504.02327",  # LearNAT: Learning NL2SQL with AST-guided Task Decomposition for Large Language Models
    "https://arxiv.org/abs/2504.02495",  # Inference-Time Scaling for Generalist Reward Modeling
    "https://arxiv.org/abs/2504.02546",  # GPG: A Simple and Strong Reinforcement Learning Baseline for Model Reasoning
    "https://arxiv.org/abs/2504.02792",  # Unified World Models: Coupling Video and Action Diffusion for Pretraining on Large Robotic Datasets
    "https://arxiv.org/abs/2504.02918",  # Morpheus: Benchmarking Physical Reasoning of Video Generative Models with Real Physical Experiments
    "https://arxiv.org/abs/2504.03118",  # NuWa: Deriving Lightweight Task-Specific Vision Transformers for Edge Devices
    "https://arxiv.org/abs/2504.03151",  # Why Reasoning Matters? A Survey of Advancements in Multimodal Reasoning (v1)
    "https://arxiv.org/abs/2504.03169",  # REJEPA: A Novel Joint-Embedding Predictive Architecture for Efficient Remote Sensing Image Retrieval
    "https://arxiv.org/abs/2504.03206",  # Enhancing Personalized Multi-Turn Dialogue with Curiosity Reward
    "https://arxiv.org/abs/2504.03515",  # Dexterous Manipulation through Imitation Learning: A Survey
    "https://arxiv.org/abs/2504.03597",  # Real-is-Sim: Bridging the Sim-to-Real Gap with a Dynamic Digital Twin
    "https://arxiv.org/abs/2504.04170",  # Digital Gene: Learning about the Physical World through Analytic Concepts
    "https://arxiv.org/abs/2504.04259",  # ORCA: An Open-Source, Reliable, Cost-Effective, Anthropomorphic Robotic Hand for Uninterrupted Dexterous Task Learning
    "https://arxiv.org/abs/2504.04675",  # HypRL: Reinforcement Learning of Control Policies for Hyperproperties
    "https://arxiv.org/abs/2504.04736",  # Synthetic Data Generation & Multi-Step RL for Reasoning & Tool Use
    "https://arxiv.org/abs/2504.05118",  # VAPO: Efficient and Reliable Reinforcement Learning for Advanced Reasoning Tasks
    "https://arxiv.org/abs/2504.05299",  # SmolVLM: Redefining small and efficient multimodal models
    "https://arxiv.org/abs/2504.05520",  # Efficient Reinforcement Finetuning via Adaptive Curriculum Learning
    "https://arxiv.org/abs/2504.05786",  # How to Enable LLM with 3D Capacity? A Survey of Spatial Reasoning in LLM
    "https://arxiv.org/abs/2504.05812",  # Right Question is Already Half the Answer: Fully Unsupervised LLM Reasoning Incentivization
    "https://arxiv.org/abs/2504.06020",  # Information-Theoretic Reward Decomposition for Generalizable RLHF
    "https://arxiv.org/abs/2504.06120",  # Hyperbolic Category Discovery
    "https://arxiv.org/abs/2504.06256",  # Transfer between Modalities with MetaQueries
    "https://arxiv.org/abs/2504.06389",  # SemiDAViL: Semi-supervised Domain Adaptation with Vision-Language Guidance for Semantic Segmentation
    "https://arxiv.org/abs/2504.06608",  # A Cross-Domain Few-Shot Learning Method Based on Domain Knowledge Mapping
    "https://arxiv.org/abs/2504.06662",  # RAMBO: RL-Augmented Model-Based Whole-Body Control for Loco-Manipulation
    "https://arxiv.org/abs/2504.07213",  # Evolutionary Machine Learning meets Self-Supervised Learning: a comprehensive survey
    "https://arxiv.org/abs/2504.07491",  # Kimi-VL Technical Report
    "https://arxiv.org/abs/2504.07615",  # VLM-R1: A Stable and Generalizable R1-style Large Vision-Language Model
    "https://arxiv.org/abs/2504.07745",  # SF2T: Self-supervised Fragment Finetuning of Video-LLMs for Fine-Grained Understanding
    "https://arxiv.org/abs/2504.07793",  # Revisiting Likelihood-Based Out-of-Distribution Detection by Modeling Representations
    "https://arxiv.org/abs/2504.07934",  # SoTA with Less: MCTS-Guided Sample Selection for Data-Efficient Visual Reasoning Self-Improvement
    "https://arxiv.org/abs/2504.07951",  # Scaling Laws for Native Multimodal Models
    "https://arxiv.org/abs/2504.07954",  # Perception-R1: Pioneering Perception Policy with Reinforcement Learning
    "https://arxiv.org/abs/2504.08600",  # SQL-R1: Training Natural Language to SQL Reasoning Model By Reinforcement Learning
    "https://arxiv.org/abs/2504.08672",  # Genius: A Generalizable and Purely Unsupervised Self-Training Framework For Advanced Reasoning
    "https://arxiv.org/abs/2504.08837",  # VL-Rethinker: Incentivizing Self-Reflection of Vision-Language Models with Reinforcement Learning
    "https://arxiv.org/abs/2504.09037",  # A Survey of Frontiers in LLM Reasoning: Inference Scaling, Learning to Reason, and Agentic Systems
    "https://arxiv.org/abs/2504.09130",  # VisuoThink: Empowering LVLM Reasoning with Multimodal Tree Search
    "https://arxiv.org/abs/2504.09532",  # Humanoid Agent via Embodied Chain-of-Action Reasoning with Multimodal Foundation Models for Zero-Shot Loco-Manipulation
    "https://arxiv.org/abs/2504.09819",  # Density-based Object Detection in Crowded Scenes
    "https://arxiv.org/abs/2504.09828",  # FATE: A Prompt-Tuning-Based Semi-Supervised Learning Framework for Extremely Limited Labeled Data
    "https://arxiv.org/abs/2504.09848",  # A Survey of Large Language Model-Powered Spatial Intelligence Across Scales: Advances in Embodied Agents, Smart Cities, and Earth Science
    "https://arxiv.org/abs/2504.09997",  # GenTe: Generative Real-world Terrains for General Legged Robot Locomotion Control
    "https://arxiv.org/abs/2504.10428",  # Learning with Positive and Imperfect Unlabeled Data
    "https://arxiv.org/abs/2504.10449",  # M1: Towards Scalable Test-Time Compute with Mamba Reasoning Models
    "https://arxiv.org/abs/2504.10462",  # The Scalability of Simplicity: Empirical Analysis of Vision-Language Learning with a Single Transformer
    "https://arxiv.org/abs/2504.10479",  # InternVL3: Exploring Advanced Training and Test-Time Recipes for Open-Source Multimodal Models
    "https://arxiv.org/abs/2504.10512",  # JEPA4Rec: Learning Effective Language Representations for Sequential Recommendation via Joint Embedding Predictive Architecture
    "https://arxiv.org/abs/2504.10903",  # Efficient Reasoning Models: A Survey
    "https://arxiv.org/abs/2504.11054",  # Zero-Shot Whole-Body Humanoid Control via Behavioral Foundation Models
    "https://arxiv.org/abs/2504.11170",  # A real-time anomaly detection method for robots based on a flexible and sparse latent space
    "https://arxiv.org/abs/2504.11343",  # A Minimalist Approach to LLM Reasoning: from Rejection Sampling to Reinforce
    "https://arxiv.org/abs/2504.11453",  # A Clean Slate for Offline Reinforcement Learning
    "https://arxiv.org/abs/2504.11456",  # DeepMath-103K: A Large-Scale, Challenging, Decontaminated, and Verifiable Mathematical Dataset for Advancing Reasoning
    "https://arxiv.org/abs/2504.11468",  # SFT or RL? An Early Investigation into Training R1-Like Reasoning Large Vision-Language Models
    "https://arxiv.org/abs/2504.11536",  # ReTool: Reinforcement Learning for Strategic Tool Use in LLMs
    "https://arxiv.org/abs/2504.12104",  # Logits DeConfusion with CLIP for Few-Shot Learning
    "https://arxiv.org/abs/2504.12216",  # d1: Scaling Reasoning in Diffusion Large Language Models via Reinforcement Learning
    "https://arxiv.org/abs/2504.12328",  # A Comprehensive Survey of Reward Models: Taxonomy, Applications, Challenges, and Future
    "https://arxiv.org/abs/2504.12369",  # WorldMem: Long-term Consistent World Simulation with Memory
    "https://arxiv.org/abs/2504.12680",  # Embodied-R: Collaborative Framework for Activating Embodied Spatial Reasoning in Foundation Models via Reinforcement Learning
    "https://arxiv.org/abs/2504.12684",  # SOPHY: Learning to Generate Simulation-Ready Objects with Physical Materials
    "https://arxiv.org/abs/2504.12717",  # Post-pre-training for Modality Alignment in Vision-Language Foundation Models
    "https://arxiv.org/abs/2504.12764",  # GraphOmni: A Comprehensive and Extensible Benchmark Framework for Large Language Models on Graph-theoretic Tasks
    "https://arxiv.org/abs/2504.13055",  # NoisyRollout: Reinforcing Visual Reasoning with Data Augmentation
    "https://arxiv.org/abs/2504.13059",  # RoboTwin: Dual-Arm Robot Benchmark with Generative Digital Twins
    "https://arxiv.org/abs/2504.13129",  # Science-T2I: Addressing Scientific Illusions in Image Synthesis
    "https://arxiv.org/abs/2504.13159",  # Digital Twin Generation from Visual Data: A Survey
    "https://arxiv.org/abs/2504.13161",  # Nemotron-CLIMB: CLustering-based Iterative Data Mixture Bootstrapping for Language Model Pre-training
    "https://arxiv.org/abs/2504.13173",  # It's All Connected: A Journey Through Test-Time Memorization, Attentional Bias, Retention, and Online Optimization
    "https://arxiv.org/abs/2504.13180",  # PerceptionLM: Open-Access Data and Models for Detailed Visual Understanding
    "https://arxiv.org/abs/2504.13181",  # Perception Encoder: The best visual embeddings are not at the output of the network
    "https://arxiv.org/abs/2504.13292",  # Let Me Grok for You: Accelerating Grokking via Embedding Transfer from a Weaker Model
    "https://arxiv.org/abs/2504.13469",  # HMPE:HeatMap Embedding for Efficient Transformer-Based Small Object Detection
    "https://arxiv.org/abs/2504.13818",  # Not All Rollouts are Useful: Down-Sampling Rollouts in LLM Reinforcement Learning
    "https://arxiv.org/abs/2504.13828",  # Generative AI Act II: Test Time Scaling Drives Cognition Engineering
    "https://arxiv.org/abs/2504.13837",  # Does Reinforcement Learning Really Incentivize Reasoning Capacity in LLMs Beyond the Base Model?
    "https://arxiv.org/abs/2504.13958",  # ToolRL: Reward is All Tool Learning Needs
    "https://arxiv.org/abs/2504.14117",  # PEFT A2Z: Parameter-Efficient Fine-Tuning Survey for Large Language and Vision Models
    "https://arxiv.org/abs/2504.14200",  # Enhancing Multimodal In-Context Learning for Image Classification through Coreset Optimization
    "https://arxiv.org/abs/2504.14920",  # DyFo: A Training-Free Dynamic Focus Visual Search for Enhancing LMMs in Fine-Grained Visual Understanding
    "https://arxiv.org/abs/2504.14945",  # Learning to Reason under Off-Policy Guidance
    "https://arxiv.org/abs/2504.14988",  # Benchmarking Large Vision-Language Models on Fine-Grained Image Tasks: A Comprehensive Evaluation
    "https://arxiv.org/abs/2504.15037",  # Scaling and Beyond: Advancing Spatial Reasoning in MLLMs Requires New Recipes
    "https://arxiv.org/abs/2504.15271",  # Eagle 2.5: Boosting Long-Context Post-Training for Frontier Vision-Language Models
    "https://arxiv.org/abs/2504.15275",  # Stop Summation: Min-Form Credit Assignment Is All Process Reward Model Needs for Reasoning
    "https://arxiv.org/abs/2504.15279",  # VisuLogic: A Benchmark for Evaluating Visual Reasoning in Multi-modal Large Language Models
    "https://arxiv.org/abs/2504.15280",  # Seeing from Another Perspective: Evaluating Multi-View Understanding in MLLMs
    "https://arxiv.org/abs/2504.15369",  # Solving New Tasks by Adapting Internet Video Knowledge
    "https://arxiv.org/abs/2504.15397",  # MirrorVerse: Pushing Diffusion Models to Realistically Reflect the World
    "https://arxiv.org/abs/2504.15595",  # Grasping Deformable Objects via Reinforcement Learning with Cross-Modal Attention to Visuo-Tactile Inputs
    "https://arxiv.org/abs/2504.15619",  # AdaViP: Aligning Multi-modal LLMs via Adaptive Vision-enhanced Preference Optimization
    "https://arxiv.org/abs/2504.15777",  # Tina: Tiny Reasoning Models via LoRA
    "https://arxiv.org/abs/2504.15932",  # Reasoning Physical Video Generation with Diffusion Timestep Tokens via Reinforcement Learning
    "https://arxiv.org/abs/2504.15965",  # From Human Memory to AI Memory: A Survey on Memory Mechanisms in the Era of LLMs
    "https://arxiv.org/abs/2504.16054",  # $π_{0.5}$: a Vision-Language-Action Model with Open-World Generalization
    "https://arxiv.org/abs/2504.16072",  # Describe Anything: Detailed Localized Image and Video Captioning
    "https://arxiv.org/abs/2504.16078",  # LLMs are Greedy Agents: Effects of RL Fine-tuning on Decision-Making Abilities
    "https://arxiv.org/abs/2504.16084",  # TTRL: Test-Time Reinforcement Learning
    "https://arxiv.org/abs/2504.16129",  # MARFT: Multi-Agent Reinforcement Fine-Tuning
    "https://arxiv.org/abs/2504.16591",  # JEPA for RL: Investigating Joint-Embedding Predictive Architectures for Reinforcement Learning
    "https://arxiv.org/abs/2504.16649",  # PP-Tac: Paper Picking Using Tactile Feedback in Dexterous Robotic Hands
    "https://arxiv.org/abs/2504.16656",  # Skywork R1V2: Multimodal Hybrid Reinforcement Learning for Reasoning
    "https://arxiv.org/abs/2504.16680",  # Uncertainty-Aware Robotic World Model Makes Offline Model-Based Reinforcement Learning Work on Real Robots
    "https://arxiv.org/abs/2504.16693",  # PIN-WM: Learning Physics-INformed World Models for Non-Prehensile Manipulation
    "https://arxiv.org/abs/2504.16801",  # Decoupled Global-Local Alignment for Improving Compositional Understanding
    "https://arxiv.org/abs/2504.16828",  # Process Reward Models That Think
    "https://arxiv.org/abs/2504.16843",  # Physically Consistent Humanoid Loco-Manipulation using Latent Diffusion Models
    "https://arxiv.org/abs/2504.16929",  # I-Con: A Unifying Framework for Representation Learning
    "https://arxiv.org/abs/2504.17040",  # DyMU: Dynamic Merging and Virtual Unmerging for Efficient VLMs
    "https://arxiv.org/abs/2504.17192",  # Paper2Code: Automating Code Generation from Scientific Papers in Machine Learning
    "https://arxiv.org/abs/2504.17207",  # Perspective-Aware Reasoning in Vision-Language Models via Mental Imagery Simulation
    "https://arxiv.org/abs/2504.17432",  # Breaking the Modality Barrier: Universal Embedding Learning with Multimodal LLMs
    "https://arxiv.org/abs/2504.18053",  # DREAM: Disentangling Risks to Enhance Safety Alignment in Multimodal Large Language Models
    "https://arxiv.org/abs/2504.18158",  # E-InMeMo: Enhanced Prompting for Visual In-Context Learning
    "https://arxiv.org/abs/2504.18397",  # Unsupervised Visual Chain-of-Thought Reasoning via Preference Optimization
    "https://arxiv.org/abs/2504.18471",  # Action Flow Matching for Continual Robot Learning
    "https://arxiv.org/abs/2504.18875",  # Generative to Agentic AI: Survey, Conceptualization, and Challenges
    "https://arxiv.org/abs/2504.18904",  # RoboVerse: Towards a Unified Platform, Dataset and Benchmark for Scalable and Generalizable Robot Learning
    "https://arxiv.org/abs/2504.19162",  # SPC: Evolving Self-Play Critic via Adversarial Games for LLM Reasoning
    "https://arxiv.org/abs/2504.19254",  # Uncertainty Quantification for Language Models: A Suite of Black-Box, White-Box, LLM Judge, and Ensemble Scorers
    "https://arxiv.org/abs/2504.19475",  # Prisma: An Open Source Toolkit for Mechanistic Interpretability in Vision and Video
    "https://arxiv.org/abs/2504.19599",  # GVPO: Group Variance Policy Optimization for Large Language Model Post-Training
    "https://arxiv.org/abs/2504.19627",  # VCM: Vision Concept Modeling Based on Implicit Contrastive Learning with Vision-Language Instruction Fine-Tuning
    "https://arxiv.org/abs/2504.19854",  # NORA: A Small Open-Sourced Generalist Vision Language Action Model for Embodied Tasks
    "https://arxiv.org/abs/2504.20024",  # SpatialReasoner: Towards Explicit and Generalizable 3D Spatial Reasoning
    "https://arxiv.org/abs/2504.20073",  # RAGEN: Understanding Self-Evolution in LLM Agents via Multi-Turn Reinforcement Learning
    "https://arxiv.org/abs/2504.20199",  # Weaving Context Across Images: Improving Vision-Language Models through Focus-Centric Visual Chains
    "https://arxiv.org/abs/2504.20364",  # Exploring internal representation of self-supervised networks: few-shot learning abilities and comparison with human semantics and recognition of objects
    "https://arxiv.org/abs/2504.20571",  # Reinforcement Learning for Reasoning in Large Language Models with One Training Example
    "https://arxiv.org/abs/2504.20595",  # ReasonIR: Training Retrievers for Reasoning Tasks
    "https://arxiv.org/abs/2504.20648",  # SpaRE: Enhancing Spatial Reasoning in Vision-Language Models with Synthetic Data
    "https://arxiv.org/abs/2504.20966",  # Softpick: No Attention Sink, No Massive Activations with Rectified Softmax
    "https://arxiv.org/abs/2504.20995",  # TesserAct: Learning 4D Embodied World Models
    "https://arxiv.org/abs/2504.20996",  # X-Fusion: Introducing New Modality to Frozen Large Language Models
    "https://arxiv.org/abs/2504.20997",  # Toward Efficient Exploration by Large Language Model Agents
    "https://arxiv.org/abs/2504.21024",  # WebEvolver: Enhancing Web Agent Self-Improvement with Coevolving World Model
    "https://arxiv.org/abs/2504.21233",  # Phi-4-Mini-Reasoning: Exploring the Limits of Small Reasoning Language Models in Math
    "https://arxiv.org/abs/2504.21277",  # Reinforced MLLM: A Survey on RL-Based Reasoning in Multimodal Large Language Models
    "https://arxiv.org/abs/2504.21318",  # Phi-4-reasoning Technical Report
    "https://arxiv.org/abs/2504.21356",  # Nexus-Gen: Unified Image Understanding, Generation, and Editing via Prefilled Autoregression in Shared Embedding Space
    "https://arxiv.org/abs/2504.21370",  # ShorterBetter: Guiding Reasoning Models to Find Optimal Inference Length for Efficient Reasoning
    "https://arxiv.org/abs/2504.21447",  # Multimodal Language Models See Better When They Look Shallower
    "https://arxiv.org/abs/2504.21559",  # Black-Box Visual Prompt Engineering for Mitigating Object Hallucination in Large Vision Language Models
    "https://arxiv.org/abs/2504.21561",  # Iterative Tool Usage Exploration for Multimodal Agents via Step-wise Preference Tuning
    "https://arxiv.org/abs/2504.21776",  # WebThinker: Empowering Large Reasoning Models with Deep Research Capability
    "https://arxiv.org/abs/2504.21801",  # DeepSeek-Prover-V2: Advancing Formal Mathematical Reasoning via Reinforcement Learning for Subgoal Decomposition
    "https://arxiv.org/abs/2504.21850",  # COMPACT: COMPositional Atomic-to-Complex Visual Capability Tuning
    "https://arxiv.org/abs/2504.21853",  # A Survey of Interactive Generative Video
    "https://arxiv.org/abs/2504.21855",  # ReVision: Refining Video Diffusion with Explicit 3D Motion Modeling
    "https://arxiv.org/abs/2505.00024",  # Nemotron-Research-Tool-N1: Exploring Tool-Using Language Models with Reinforced Reasoning
    "https://arxiv.org/abs/2505.00147",  # AdaptMI: Adaptive Skill-based In-context Math Instruction for Small Language Models
    "https://arxiv.org/abs/2505.00209",  # Direct Motion Models for Assessing Generated Videos
    "https://arxiv.org/abs/2505.00315",  # Mixture of Sparse Attention: Content-Based Learnable Sparse Attention via Expert-Choice Routing
    "https://arxiv.org/abs/2505.00337",  # T2VPhysBench: A First-Principles Benchmark for Physical Consistency in Text-to-Video Generation
    "https://arxiv.org/abs/2505.00551",  # 100 Days After DeepSeek-R1: A Survey on Replication Studies and More Directions for Reasoning Language Models
    "https://arxiv.org/abs/2505.00703",  # T2I-R1: Reinforcing Image Generation with Collaborative Semantic-level and Token-level CoT
    "https://arxiv.org/abs/2505.00779",  # Uncertainty-aware Latent Safety Filters for Avoiding Out-of-Distribution Failures
    "https://arxiv.org/abs/2505.00787",  # Constructing an Optimal Behavior Basis for the Option Keyboard
    "https://arxiv.org/abs/2505.00788",  # SpatialLLM: A Compound 3D-Informed Design towards Spatially-Intelligent Large Multimodal Models
    "https://arxiv.org/abs/2505.00949",  # Llama-Nemotron: Efficient Reasoning Models
    "https://arxiv.org/abs/2505.00991",  # DexCtrl: Towards Sim-to-Real Dexterity with Adaptive Controller Learning
    "https://arxiv.org/abs/2505.01064",  # Efficient Vocabulary-Free Fine-Grained Visual Recognition in the Age of Multimodal LLMs
    "https://arxiv.org/abs/2505.01441",  # Agentic Reasoning and Tool Integration for LLMs via Reinforcement Learning
    "https://arxiv.org/abs/2505.01812",  # $\\textit{New News}$: System-2 Fine-tuning for Robust Integration of New Knowledge
    "https://arxiv.org/abs/2505.01822",  # Analytic Energy-Guided Policy Optimization for Offline Reinforcement Learning
    "https://arxiv.org/abs/2505.01996",  # Always Skip Attention
    "https://arxiv.org/abs/2505.02056",  # Handling Imbalanced Pseudolabels for Vision-Language Models with Concept Alignment and Confusion-Aware Calibrated Margin
    "https://arxiv.org/abs/2505.02152",  # Interleave-VLA: Enhancing Robot Manipulation with Interleaved Image-Text Instructions
    "https://arxiv.org/abs/2505.02222",  # Practical Efficiency of Muon for Pretraining
    "https://arxiv.org/abs/2505.02278",  # Compositional Image-Text Matching and Retrieval by Grounding Entities
    "https://arxiv.org/abs/2505.02387",  # RM-R1: Reward Modeling as Reasoning
    "https://arxiv.org/abs/2505.02391",  # Optimizing Chain-of-Thought Reasoners via Gradient Variance Minimization in Rejection Sampling and RL
    "https://arxiv.org/abs/2505.02406",  # Token Coordinated Prompt Attention is Needed for Visual Prompting
    "https://arxiv.org/abs/2505.02567",  # Unified Multimodal Understanding and Generation Models: Advances, Challenges, and Opportunities
    "https://arxiv.org/abs/2505.02665",  # A Survey of Slow Thinking-based Reasoning LLMs using Reinforced Learning and Inference-time Scaling Law
    "https://arxiv.org/abs/2505.02831",  # No Other Representation Component Is Needed: Diffusion Transformers Can Provide Representation Guidance by Themselves
    "https://arxiv.org/abs/2505.02835",  # R1-Reward: Training Multimodal Reward Model Through Stable Reinforcement Learning
    "https://arxiv.org/abs/2505.03113",  # Image Recognition with Online Lightweight Vision Transformer: A Survey
    "https://arxiv.org/abs/2505.03176",  # seq-JEPA: Autoregressive Predictive Learning of Invariant-Equivariant World Models
    "https://arxiv.org/abs/2505.03181",  # VLM Q-Learning: Aligning Vision-Language Models for Interactive Decision-Making
    "https://arxiv.org/abs/2505.03233",  # GraspVLA: a Grasping Foundation Model Pre-trained on Billion-scale Synthetic Action Data
    "https://arxiv.org/abs/2505.03238",  # RobotxR1: Enabling Embodied Robotic Intelligence on Large Language Models through Closed-Loop Reinforcement Learning
    "https://arxiv.org/abs/2505.03318",  # Unified Multimodal Chain-of-Thought Reward Model through Reinforcement Fine-Tuning
    "https://arxiv.org/abs/2505.03335",  # Absolute Zero: Reinforced Self-play Reasoning with Zero Data
    "https://arxiv.org/abs/2505.03500",  # Task Reconstruction and Extrapolation for $π_0$ using Text Latent
    "https://arxiv.org/abs/2505.03586",  # Rainbow Delay Compensation: A Multi-Agent Reinforcement Learning Framework for Mitigating Delayed Observation
    "https://arxiv.org/abs/2505.03703",  # Fill the Gap: Quantifying and Reducing the Modality Gap in Image-Text Representation Learning
    "https://arxiv.org/abs/2505.03981",  # X-Reasoner: Towards Generalizable Reasoning Across Modalities and Domains
    "https://arxiv.org/abs/2505.04410",  # DeCLIP: Decoupled Learning for Open-Vocabulary Dense Perception
    "https://arxiv.org/abs/2505.04588",  # ZeroSearch: Incentivize the Search Capability of LLMs without Searching
    "https://arxiv.org/abs/2505.04601",  # OpenVision: A Fully-Open, Cost-Effective Family of Advanced Vision Encoders for Multimodal Learning
    "https://arxiv.org/abs/2505.04769",  # Vision-Language-Action (VLA) Models: Concepts, Progress, Applications and Challenges
    "https://arxiv.org/abs/2505.04860",  # D-CODA: Diffusion for Coordinated Dual-Arm Data Augmentation
    "https://arxiv.org/abs/2505.04921",  # Perception, Reason, Think, and Plan: A Survey on Large Multimodal Reasoning Models
    "https://arxiv.org/abs/2505.05062",  # ULFine: Unbiased Lightweight Fine-tuning for Foundation-Model-Assisted Long-Tailed Semi-Supervised Learning
    "https://arxiv.org/abs/2505.05108",  # Multi-agent Embodied AI: Advances and Future Directions
    "https://arxiv.org/abs/2505.05177",  # MARK: Memory Augmented Refinement of Knowledge
    "https://arxiv.org/abs/2505.05422",  # TokLIP: Marry Visual Tokens to CLIP for Multimodal Comprehension and Generation
    "https://arxiv.org/abs/2505.05456",  # SITE: towards Spatial Intelligence Thorough Evaluation
    "https://arxiv.org/abs/2505.05464",  # Bring Reason to Vision: Understanding Perception and Reasoning through Model Merging
    "https://arxiv.org/abs/2505.05469",  # Generating Physically Stable and Buildable Brick Structures from Text
    "https://arxiv.org/abs/2505.05470",  # Flow-GRPO: Training Flow Matching Models via Online RL
    "https://arxiv.org/abs/2505.05472",  # Mogao: An Omni Foundation Model for Interleaved Multi-Modal Generation
    "https://arxiv.org/abs/2505.05495",  # Learning 3D Persistent Embodied World Models
    "https://arxiv.org/abs/2505.05512",  # Occupancy World Model for Robots
    "https://arxiv.org/abs/2505.05522",  # Continuous Thought Machines
    "https://arxiv.org/abs/2505.05626",  # Perceiving Beyond Language Priors: Enhancing Visual Comprehension and Attention in Multimodal Models
    "https://arxiv.org/abs/2505.05753",  # Towards Embodiment Scaling Laws in Robot Locomotion
    "https://arxiv.org/abs/2505.05787",  # Demystifying Diffusion Policies: Action Memorization and Simple Lookup Table Alternatives
    "https://arxiv.org/abs/2505.05800",  # 3D CAVLA: Leveraging Depth and 3D Context to Generalize Vision Language Action Models for Unseen Tasks
    "https://arxiv.org/abs/2505.05811",  # Unsupervised Anomaly Detection for Autonomous Robots via Mahalanobis SVDD with Audio-IMU Fusion
    "https://arxiv.org/abs/2505.06111",  # UniVLA: Learning to Act Anywhere with Task-centric Latent Actions
    "https://arxiv.org/abs/2505.06120",  # LLMs Get Lost In Multi-Turn Conversation
    "https://arxiv.org/abs/2505.06182",  # Apple: Toward General Active Perception via Reinforcement Learning
    "https://arxiv.org/abs/2505.06451",  # Adaptive Wiping: Adaptive contact-rich manipulation through few-shot imitation learning with Force-Torque feedback and pre-trained object representations
    "https://arxiv.org/abs/2505.06708",  # Gated Attention for Large Language Models: Non-linearity, Sparsity, and Attention-Sink-Free
    "https://arxiv.org/abs/2505.06776",  # FALCON: Learning Force-Adaptive Humanoid Loco-Manipulation
    "https://arxiv.org/abs/2505.06890",  # Image Classification Using a Diffusion Model as a Pre-Training Model
    "https://arxiv.org/abs/2505.07062",  # Seed1.5-VL Technical Report
    "https://arxiv.org/abs/2505.07233",  # DynamicRAG: Leveraging Outputs of Large Language Model as Feedback for Dynamic Reranking in Retrieval-Augmented Generation
    "https://arxiv.org/abs/2505.07291",  # INTELLECT-2: A Reasoning Model Trained Through Globally Decentralized Reinforcement Learning
    "https://arxiv.org/abs/2505.07538",  # Selftok: Discrete Visual Tokens of Autoregression, by Diffusion, and for Reasoning
    "https://arxiv.org/abs/2505.07634",  # Neural Brain: A Neuroscience-inspired Framework for Embodied Agents
    "https://arxiv.org/abs/2505.07675",  # Simple yet Effective Semi-supervised Knowledge Distillation from Vision-Language Models via Dual-Head Optimization
    "https://arxiv.org/abs/2505.07773",  # Agent RL Scaling Law: Agent RL with Spontaneous Code Execution for Mathematical Problem Solving
    "https://arxiv.org/abs/2505.07956",  # Symbolic Regression with Multimodal Large Language Models and Kolmogorov Arnold Networks
    "https://arxiv.org/abs/2505.08022",  # Dynamical Low-Rank Compression of Neural Networks with Robustness under Adversarial Attacks
    "https://arxiv.org/abs/2505.08078",  # What Matters for Batch Online Reinforcement Learning in Robotics?
    "https://arxiv.org/abs/2505.08548",  # From Seeing to Doing: Bridging Reasoning and Decision for Robotic Manipulation
    "https://arxiv.org/abs/2505.08617",  # OpenThinkIMG: Learning to Think with Images via Visual Tool Reinforcement Learning
    "https://arxiv.org/abs/2505.08971",  # Prioritizing Image-Related Tokens Enhances Vision-Language Pre-Training
    "https://arxiv.org/abs/2505.09316",  # Scent of Knowledge: Optimizing Search-Enhanced Reasoning with Information Foraging
    "https://arxiv.org/abs/2505.09343",  # Insights into DeepSeek-V3: Scaling Challenges and Reflections on Hardware for AI Architectures
    "https://arxiv.org/abs/2505.09561",  # Learning Long-Context Diffusion Policies via Past-Token Prediction
    "https://arxiv.org/abs/2505.09568",  # BLIP3-o: A Family of Fully Open Unified Multimodal Models-Architecture, Training and Dataset
    "https://arxiv.org/abs/2505.09577",  # VTLA: Vision-Tactile-Language-Action Model with Preference Learning for Insertion Manipulation
    "https://arxiv.org/abs/2505.09651",  # Unlocking Location Intelligence: A Survey from Deep Learning to The LLM Era
    "https://arxiv.org/abs/2505.09694",  # EWMBench: Evaluating Scene, Motion, and Semantic Quality in Embodied World Models
    "https://arxiv.org/abs/2505.09723",  # EnerVerse-AC: Envisioning Embodied Environments with Action Condition
    "https://arxiv.org/abs/2505.10007",  # Sample Complexity of Distributionally Robust Average-Reward Reinforcement Learning
    "https://arxiv.org/abs/2505.10075",  # FlowDreamer: A RGB-D World Model with Flow-based Motion Representations for Robot Manipulation
    "https://arxiv.org/abs/2505.10088",  # MMRL++: Parameter-Efficient and Interaction-Aware Representation Learning for Vision-Language Models
    "https://arxiv.org/abs/2505.10320",  # J1: Incentivizing Thinking in LLM-as-a-Judge via Reinforcement Learning
    "https://arxiv.org/abs/2505.10425",  # Learning to Think: Information-Theoretic Reinforcement Fine-Tuning for LLMs
    "https://arxiv.org/abs/2505.10446",  # Reinforcing the Diffusion Chain of Lateral Thought with Diffusion Language Models
    "https://arxiv.org/abs/2505.10465",  # Superposition Yields Robust Neural Scaling
    "https://arxiv.org/abs/2505.10468",  # AI Agents vs. Agentic AI: A Conceptual Taxonomy, Applications and Challenges
    "https://arxiv.org/abs/2505.10526",  # MASSV: Multimodal Adaptation and Self-Data Distillation for Speculative Decoding of Vision-Language Models
    "https://arxiv.org/abs/2505.10557",  # MathCoder-VL: Bridging Vision and Code for Enhanced Multimodal Mathematical Reasoning
    "https://arxiv.org/abs/2505.10559",  # Neural Thermodynamic Laws for Large Language Model Training
    "https://arxiv.org/abs/2505.10755",  # Procedural Generation of Articulated Simulation-Ready Assets
    "https://arxiv.org/abs/2505.10832",  # Learning When to Think: Shaping Adaptive Reasoning in R1-Style Models via Multi-Stage RL
    "https://arxiv.org/abs/2505.10881",  # Prior-Guided Diffusion Planning for Offline Reinforcement Learning
    "https://arxiv.org/abs/2505.10947",  # Certifying Stability of Reinforcement Learning Policies using Generalized Lyapunov Functions
    "https://arxiv.org/abs/2505.10978",  # Group-in-Group Policy Optimization for LLM Agent Training
    "https://arxiv.org/abs/2505.11032",  # DexGarmentLab: Dexterous Garment Manipulation Environment with Generalizable Policy
    "https://arxiv.org/abs/2505.11081",  # ShiQ: Bringing back Bellman to LLMs
    "https://arxiv.org/abs/2505.11123",  # Conditioning Matters: Training Diffusion Policies is Faster Than You Think
    "https://arxiv.org/abs/2505.11129",  # PhiNet v2: A Mask-Free Brain-Inspired Vision Foundation Model from Video
    "https://arxiv.org/abs/2505.11192",  # FALCON: False-Negative Aware Learning of Contrastive Negatives in Vision-Language Alignment
    "https://arxiv.org/abs/2505.11221",  # Sample Efficient Reinforcement Learning via Large Vision Language Model Distillation
    "https://arxiv.org/abs/2505.11227",  # Is PRM Necessary? Problem-Solving RL Implicitly Induces PRM Capability in LLMs
    "https://arxiv.org/abs/2505.11383",  # Dynam3D: Dynamic Layered 3D Tokens Empower VLM for Vision-and-Language Navigation
    "https://arxiv.org/abs/2505.11409",  # Visual Planning: Let's Think Only with Images
    "https://arxiv.org/abs/2505.11484",  # SoftCoT++: Test-Time Scaling with Soft Chain-of-Thought Reasoning
    "https://arxiv.org/abs/2505.11494",  # SHIELD: Safety on Humanoids via CBFs In Expectation on Learned Dynamics
    "https://arxiv.org/abs/2505.11528",  # LaDi-WM: A Latent Diffusion-based World Model for Predictive Manipulation
    "https://arxiv.org/abs/2505.11614",  # Using Reinforcement Learning to Train Large Language Models to Explain Human Decisions
    "https://arxiv.org/abs/2505.11709",  # EgoDex: Learning Dexterous Manipulation from Large-Scale Egocentric Video
    "https://arxiv.org/abs/2505.11711",  # Reinforcement Learning Finetunes Small Subnetworks in Large Language Models
    "https://arxiv.org/abs/2505.11792",  # Solver-Informed RL: Grounding Large Language Models for Authentic Optimization Modeling
    "https://arxiv.org/abs/2505.11815",  # UniMoCo: Unified Modality Completion for Robust Multi-Modal Embeddings
    "https://arxiv.org/abs/2505.11816",  # Continuous Subspace Optimization for Continual Learning
    "https://arxiv.org/abs/2505.11820",  # Chain-of-Model Learning for Language Model
    "https://arxiv.org/abs/2505.11858",  # Integrating Model-based Control and RL for Sim2Real Transfer of Tight Insertion Policies
    "https://arxiv.org/abs/2505.11896",  # AdaCoT: Pareto-Optimal Adaptive Chain-of-Thought Triggering via Reinforcement Learning
    "https://arxiv.org/abs/2505.11907",  # Are Multimodal Large Language Models Ready for Omnidirectional Spatial Reasoning?
    "https://arxiv.org/abs/2505.11917",  # OneTwoVLA: A Unified Vision-Language-Action Model with Adaptive Reasoning
    "https://arxiv.org/abs/2505.12081",  # VisionReasoner: Unified Reasoning-Integrated Visual Perception via Reinforcement Learning
    "https://arxiv.org/abs/2505.12082",  # Model Merging in Pre-training of Large Language Models
    "https://arxiv.org/abs/2505.12224",  # RoboFAC: A Comprehensive Framework for Robotic Failure Analysis and Correction
    "https://arxiv.org/abs/2505.12285",  # CALM: Co-evolution of Algorithms and Language Model for Automatic Heuristic Design
    "https://arxiv.org/abs/2505.12294",  # PartDexTOG: Generating Dexterous Task-Oriented Grasping via Language-driven Part Analysis
    "https://arxiv.org/abs/2505.12312",  # Visuospatial Cognitive Assistant
    "https://arxiv.org/abs/2505.12363",  # Towards Visuospatial Cognition via Hierarchical Fusion of Visual Experts
    "https://arxiv.org/abs/2505.12366",  # DisCO: Reinforcing Large Reasoning Models with Discriminative Constrained Optimization
    "https://arxiv.org/abs/2505.12370",  # Enhancing Visual Grounding for GUI Agents via Self-Evolutionary Reinforcement Learning
    "https://arxiv.org/abs/2505.12434",  # VideoRFT: Incentivizing Video Reasoning Capability in MLLMs via Reinforced Fine-Tuning
    "https://arxiv.org/abs/2505.12448",  # SSR: Enhancing Depth Perception in Vision-Language Models via Rationale-Guided Spatial Reasoning
    "https://arxiv.org/abs/2505.12477",  # Joint Embedding vs Reconstruction: Provable Benefits of Latent Space Prediction for Self Supervised Learning
    "https://arxiv.org/abs/2505.12493",  # GUI-Shift: Enhancing VLM-Based GUI Agents through Self-supervised Reinforcement Learning
    "https://arxiv.org/abs/2505.12514",  # Reasoning by Superposition: A Theoretical Perspective on Chain of Continuous Thought
    "https://arxiv.org/abs/2505.12672",  # TransferTraj: A Vehicle Trajectory Learning Model for Region and Task Transferability
    "https://arxiv.org/abs/2505.12705",  # DreamGen: Unlocking Generalization in Robot Learning through Video World Models
    "https://arxiv.org/abs/2505.12707",  # PLAICraft: Large-Scale Time-Aligned Vision-Speech-Action Dataset for Embodied AI
    "https://arxiv.org/abs/2505.12723",  # On-Policy Optimization with Group Equivalent Preference for Multi-Programming Language Understanding
    "https://arxiv.org/abs/2505.12737",  # Option-aware Temporally Abstracted Value for Offline Goal-Conditioned Reinforcement Learning
    "https://arxiv.org/abs/2505.12748",  # TeleOpBench: A Simulator-Centric Benchmark for Dual-Arm Dexterous Teleoperation
    "https://arxiv.org/abs/2505.12886",  # Detection and Mitigation of Hallucination in Large Reasoning Models: A Mechanistic Perspective
    "https://arxiv.org/abs/2505.12929",  # Do Not Let Low-Probability Tokens Over-Dominate in RL for LLMs
    "https://arxiv.org/abs/2505.13031",  # MindOmni: Unleashing Reasoning Generation in Vision Language Models with RGPO
    "https://arxiv.org/abs/2505.13138",  # Neurosymbolic Diffusion Models
    "https://arxiv.org/abs/2505.13308",  # Seek in the Dark: Reasoning via Test-Time Instance-Level Policy Gradient in Latent Space
    "https://arxiv.org/abs/2505.13317",  # Unlabeled Data vs. Pre-trained Knowledge: Rethinking SSL in the Era of Large Models
    "https://arxiv.org/abs/2505.13379",  # Thinkless: LLM Learns When to Think
    "https://arxiv.org/abs/2505.13437",  # FinePhys: Fine-grained Human Action Generation by Explicitly Incorporating Physical Laws for Effective Skeletal Guidance
    "https://arxiv.org/abs/2505.13438",  # Optimizing Anytime Reasoning via Budget Relative Policy Optimization
    "https://arxiv.org/abs/2505.13441",  # GraspMolmo: Generalizable Task-Oriented Grasping via Large-Scale Synthetic Data Generation
    "https://arxiv.org/abs/2505.13445",  # Trust, But Verify: A Self-Verification Approach to Reinforcement Learning with Verifiable Rewards
    "https://arxiv.org/abs/2505.13447",  # Mean Flows for One-step Generative Modeling
    "https://arxiv.org/abs/2505.13584",  # Self-Supervised Learning for Image Segmentation: A Comprehensive Survey
    "https://arxiv.org/abs/2505.13631",  # Learning (Approximately) Equivariant Networks via Constrained Optimization
    "https://arxiv.org/abs/2505.13696",  # Building spatial world models from sparse transitional episodic memories
    "https://arxiv.org/abs/2505.13709",  # Policy-Driven World Model Adaptation for Robust Offline Model-based Reinforcement Learning
    "https://arxiv.org/abs/2505.13840",  # EfficientLLM: Efficiency in Large Language Models
    "https://arxiv.org/abs/2505.13925",  # Time Reversal Symmetry for Efficient Robotic Manipulations in Deep Reinforcement Learning
    "https://arxiv.org/abs/2505.13934",  # RLVR-World: Training World Models with Reinforcement Learning
    "https://arxiv.org/abs/2505.13948",  # Memory-Centric Embodied Question Answering
    "https://arxiv.org/abs/2505.13975",  # DRP: Distilled Reasoning Pruning with Skill-aware Step Decomposition for Efficient Large Reasoning Models
    "https://arxiv.org/abs/2505.14030",  # AutoBio: A Simulation and Benchmark for Robotic Automation in Digital Biology Laboratory
    "https://arxiv.org/abs/2505.14069",  # Process vs. Outcome Reward: Which is Better for Agentic RAG Reinforcement Learning
    "https://arxiv.org/abs/2505.14140",  # RL of Thoughts: Navigating LLM Reasoning with Inference-time Reinforcement Learning
    "https://arxiv.org/abs/2505.14185",  # Safety Subspaces are Not Linearly Distinct: A Fine-Tuning Case Study
    "https://arxiv.org/abs/2505.14204",  # Beginning with You: Perceptual-Initialization Improves Vision-Language Representation and Alignment
    "https://arxiv.org/abs/2505.14231",  # UniVG-R1: Reasoning Guided Universal Visual Grounding with Reinforcement Learning
    "https://arxiv.org/abs/2505.14246",  # Visual Agentic Reinforcement Fine-Tuning
    "https://arxiv.org/abs/2505.14266",  # Sampling-Based System Identification with Active Exploration for Legged Robot Sim2Real Learning
    "https://arxiv.org/abs/2505.14362",  # DeepEyes: Incentivizing \"Thinking with Images\" via Reinforcement Learning
    "https://arxiv.org/abs/2505.14404",  # ViC-Bench: Benchmarking Visual-Interleaved Chain-of-Thought Capability in MLLMs with Free-Style Intermediate State Representations
    "https://arxiv.org/abs/2505.14552",  # KORGym: A Dynamic Game Platform for LLM Reasoning Evaluation
    "https://arxiv.org/abs/2505.14631",  # Think Only When You Need with Large Hybrid-Reasoning Models
    "https://arxiv.org/abs/2505.14674",  # Reward Reasoning Model
    "https://arxiv.org/abs/2505.14677",  # Visionary-R1: Mitigating Shortcuts in Visual Reasoning with Reinforcement Learning
    "https://arxiv.org/abs/2505.14683",  # Emerging Properties in Unified Multimodal Pretraining
    "https://arxiv.org/abs/2505.14684",  # Mind the Gap: Bridging Thought Leap for Improved Chain-of-Thought Tuning
    "https://arxiv.org/abs/2505.14970",  # Self-Evolving Curriculum for LLM Reasoning
    "https://arxiv.org/abs/2505.14975",  # Flattening Hierarchies with Policy Bootstrapping
    "https://arxiv.org/abs/2505.14986",  # AnyBody: A Benchmark Suite for Cross-Embodiment Manipulation
    "https://arxiv.org/abs/2505.15034",  # RL Tango: Reinforcing Generator and Verifier Together for Language Reasoning
    "https://arxiv.org/abs/2505.15045",  # Diffusion vs. Autoregressive Language Models: A Text Embedding Perspective
    "https://arxiv.org/abs/2505.15093",  # Steering Generative Models with Experimental Data for Protein Fitness Optimization
    "https://arxiv.org/abs/2505.15134",  # The Unreasonable Effectiveness of Entropy Minimization in LLM Reasoning
    "https://arxiv.org/abs/2505.15146",  # lmgame-Bench: How Good are LLMs at Playing Games?
    "https://arxiv.org/abs/2505.15211",  # GCNT: Graph-Based Transformer Policies for Morphology-Agnostic Reinforcement Learning
    "https://arxiv.org/abs/2505.15257",  # When Less Language is More: Language-Reasoning Disentanglement Makes LLMs Better Multilingual Reasoners
    "https://arxiv.org/abs/2505.15311",  # Trajectory Bellman Residual Minimization: A Simple Value-Based Method for LLM Reasoning
    "https://arxiv.org/abs/2505.15345",  # Hadamax Encoding: Elevating Performance in Model-Free Atari
    "https://arxiv.org/abs/2505.15418",  # Guided Policy Optimization under Partial Observability
    "https://arxiv.org/abs/2505.15436",  # Adaptive Chain-of-Focus Reasoning via Dynamic Visual Search and Zooming for Efficient VLMs
    "https://arxiv.org/abs/2505.15456",  # Teaching Language Models to Evolve with Users: Dynamic Profile Modeling for Personalized Alignment
    "https://arxiv.org/abs/2505.15506",  # Prompt Tuning Vision Language Models with Margin Regularizer for Few-Shot Learning under Distribution Shifts
    "https://arxiv.org/abs/2505.15510",  # Visual Thoughts: A Unified Perspective of Understanding Multimodal Chain-of-Thought
    "https://arxiv.org/abs/2505.15544",  # A Temporal Difference Method for Stochastic Continuous Dynamics
    "https://arxiv.org/abs/2505.15589",  # World Models as Reference Trajectories for Rapid Motor Adaptation
    "https://arxiv.org/abs/2505.15612",  # Learn to Reason Efficiently with Adaptive Length-based Reward Shaping
    "https://arxiv.org/abs/2505.15659",  # FLARE: Robot Learning with Implicit World Modeling
    "https://arxiv.org/abs/2505.15660",  # Exploring the Limits of Vision-Language-Action Manipulations in Cross-task Generalization
    "https://arxiv.org/abs/2505.15754",  # Improving planning and MBRL with temporally-extended actions
    "https://arxiv.org/abs/2505.15795",  # Reverse Engineering Human Preferences with Reinforcement Learning
    "https://arxiv.org/abs/2505.15801",  # VerifyBench: Benchmarking Reference-based Reward Systems for Large Language Models
    "https://arxiv.org/abs/2505.15804",  # STAR-R1: Spatial TrAnsformation Reasoning by Reinforcing Multimodal LLMs
    "https://arxiv.org/abs/2505.15809",  # MMaDA: Multimodal Large Diffusion Language Models
    "https://arxiv.org/abs/2505.15810",  # GUI-G1: Understanding R1-Zero-Like Training for Visual Grounding in GUI Agents
    "https://arxiv.org/abs/2505.15879",  # GRIT: Teaching MLLMs to Think with Images
    "https://arxiv.org/abs/2505.15929",  # PhyX: Does Your Model Have the "Wits" for Physical Reasoning?
    "https://arxiv.org/abs/2505.15966",  # Pixel Reasoner: Incentivizing Pixel-Space Reasoning with Curiosity-Driven Reinforcement Learning
    "https://arxiv.org/abs/2505.15970",  # Analyzing Hierarchical Structure in Vision Models with Sparse Autoencoders
    "https://arxiv.org/abs/2505.16053",  # Learning from Algorithm Feedback: One-Shot SAT Solver Guidance with GNNs
    "https://arxiv.org/abs/2505.16149",  # When VLMs Meet Image Classification: Test Sets Renovation via Missing Label Identification
    "https://arxiv.org/abs/2505.16151",  # Training-Free Reasoning and Reflection in MLLMs
    "https://arxiv.org/abs/2505.16186",  # SafeKey: Amplifying Aha-Moment Insights for Safety Reasoning
    "https://arxiv.org/abs/2505.16192",  # VLM-R$^3$: Region Recognition, Reasoning, and Refinement for Enhanced Multimodal Chain-of-Thought
    "https://arxiv.org/abs/2505.16196",  # SEM: Enhancing Spatial Understanding for Robust Robot Manipulation
    "https://arxiv.org/abs/2505.16217",  # Reward-Aware Proto-Representations in Reinforcement Learning
    "https://arxiv.org/abs/2505.16249",  # Manipulating Elasto-Plastic Objects With 3D Occupancy and Learning-Based Predictive Control
    "https://arxiv.org/abs/2505.16278",  # DriveMoE: Mixture-of-Experts for Vision-Language-Action Model in End-to-End Autonomous Driving
    "https://arxiv.org/abs/2505.16315",  # Incentivizing Dual Process Thinking for Efficient Large Language Model Reasoning
    "https://arxiv.org/abs/2505.16368",  # SATURN: SAT-based Reinforcement Learning to Unleash LLMs Reasoning
    "https://arxiv.org/abs/2505.16394",  # Raw2Drive: Reinforcement Learning with Aligned World Models for End-to-End Autonomous Driving (in CARLA v2)
    "https://arxiv.org/abs/2505.16411",  # Mitigating Hallucinations in Vision-Language Models through Image-Guided Head Suppression
    "https://arxiv.org/abs/2505.16416",  # Circle-RoPE: Cone-like Decoupled Rotary Positional Embedding for Large Vision-Language Models
    "https://arxiv.org/abs/2505.16456",  # PhyMAGIC: Physical Motion-Aware Generative Inference with Confidence-guided LLM
    "https://arxiv.org/abs/2505.16517",  # ManipLVM-R1: Reinforcement Learning for Reasoning in Embodied Manipulation with Large Vision-Language Models
    "https://arxiv.org/abs/2505.16548",  # Incremental Sequence Classification with Temporal Consistency
    "https://arxiv.org/abs/2505.16552",  # Think Silently, Think Fast: Dynamic Latent Compression of LLM Reasoning Chains
    "https://arxiv.org/abs/2505.16579",  # Bridging the Dynamic Perception Gap: Training-Free Draft Chain-of-Thought for Dynamic Multimodal Spatial Reasoning
    "https://arxiv.org/abs/2505.16581",  # How Ensembles of Distilled Policies Improve Generalisation in Reinforcement Learning
    "https://arxiv.org/abs/2505.16640",  # BadVLA: Towards Backdoor Attacks on Vision-Language-Action Models via Objective-Decoupled Optimization
    "https://arxiv.org/abs/2505.16673",  # R1-ShareVL: Incentivizing Reasoning Capability of Multimodal Large Language Models via Share-GRPO
    "https://arxiv.org/abs/2505.16782",  # Reasoning Beyond Language: A Comprehensive Survey on Latent Chain-of-Thought Reasoning
    "https://arxiv.org/abs/2505.16826",  # KTAE: A Model-Free Algorithm to Key-Tokens Advantage Estimation in Mathematical Reasoning
    "https://arxiv.org/abs/2505.16854",  # Think or Not? Selective Reasoning via Reinforcement Learning for Vision-Language Models
    "https://arxiv.org/abs/2505.16932",  # The Polar Express: Optimal Matrix Sign Methods and Their Application to the Muon Algorithm
    "https://arxiv.org/abs/2505.16933",  # LLaDA-V: Large Language Diffusion Models with Visual Instruction Tuning
    "https://arxiv.org/abs/2505.16938",  # InternAgent: When Agent Becomes the Scientist -- Building Closed-Loop System from Hypothesis to Verification
    "https://arxiv.org/abs/2505.16971",  # UniPhy: Learning a Unified Constitutive Model for Inverse Physics Simulation
    "https://arxiv.org/abs/2505.16993",  # Native Segmentation Vision Transformers
    "https://arxiv.org/abs/2505.16994",  # R$^2$ec: Towards Large Recommender Models with Reasoning
    "https://arxiv.org/abs/2505.17006",  # CoMo: Learning Continuous Latent Motion from Internet Videos for Scalable Robot Learning
    "https://arxiv.org/abs/2505.17012",  # SpatialScore: Towards Comprehensive Evaluation for Spatial Intelligence
    "https://arxiv.org/abs/2505.17015",  # Multi-SpatialMLLM: Multi-Frame Spatial Understanding with Multi-Modal Large Language Models
    "https://arxiv.org/abs/2505.17016",  # Interactive Post-Training for Vision-Language-Action Models
    "https://arxiv.org/abs/2505.17017",  # Delving into RL for Image Generation with CoT: A Study on DPO vs. GRPO
    "https://arxiv.org/abs/2505.17018",  # SophiaVL-R1: Reinforcing MLLMs Reasoning with Thinking Reward
    "https://arxiv.org/abs/2505.17022",  # GoT-R1: Unleashing Reasoning Capability of MLLM for Visual Generation with Reinforcement Learning
    "https://arxiv.org/abs/2505.17083",  # Scale-invariant Attention
    "https://arxiv.org/abs/2505.17312",  # AdaReasoner: Adaptive Reasoning Enables More Flexible Thinking in Large Language Models
    "https://arxiv.org/abs/2505.17316",  # Analyzing Fine-Grained Alignment and Enhancing Vision Understanding in Multimodal Language Models
    "https://arxiv.org/abs/2505.17508",  # On the Design of KL-Regularized Policy Gradient Algorithms for LLM Reasoning
    "https://arxiv.org/abs/2505.17534",  # Co-Reinforcement Learning for Unified Multimodal Understanding and Generation
    "https://arxiv.org/abs/2505.17540",  # RePrompt: Reasoning-Augmented Reprompting for Text-to-Image Generation via Reinforcement Learning
    "https://arxiv.org/abs/2505.17685",  # FutureSightDrive: Thinking Visually with Spatio-Temporal CoT for Autonomous Driving
    "https://arxiv.org/abs/2505.17697",  # Activation Control for Efficiently Eliciting Long Chain-of-thought Ability of Language Models
    "https://arxiv.org/abs/2505.17746",  # Fast Quiet-STaR: Thinking Without Thought Tokens
    "https://arxiv.org/abs/2505.17749",  # Mind the GAP! The Challenges of Scale in Pixel-based Deep Reinforcement Learning
    "https://arxiv.org/abs/2505.17812",  # Seeing It or Not? Interpretable Vision-aware Latent Steering to Mitigate Object Hallucinations
    "https://arxiv.org/abs/2505.17863",  # The emergence of sparse attention: impact of data distribution and benefits of repetition
    "https://arxiv.org/abs/2505.17866",  # DesignX: Human-Competitive Algorithm Designer for Black-Box Optimization
    "https://arxiv.org/abs/2505.17966",  # Is Single-View Mesh Reconstruction Ready for Robotics?
    "https://arxiv.org/abs/2505.18000",  # Anytime-valid, Bayes-assisted, Prediction-Powered Inference
    "https://arxiv.org/abs/2505.18098",  # Planning without Search: Refining Frontier LLMs with Offline Goal-Conditioned RL
    "https://arxiv.org/abs/2505.18116",  # NFT: Bridging Supervised Learning and Reinforcement Learning in Math Reasoning
    "https://arxiv.org/abs/2505.18129",  # One RL to See Them All: Visual Triple Unified Reinforcement Learning
    "https://arxiv.org/abs/2505.18151",  # WonderPlay: Dynamic 3D Scene Generation from a Single Image and Actions
    "https://arxiv.org/abs/2505.18190",  # PhySense: Sensor Placement Optimization for Accurate Physics Sensing
    "https://arxiv.org/abs/2505.18361",  # Task-Optimized Convolutional Recurrent Networks Align with Tactile Processing in the Rodent Brain
    "https://arxiv.org/abs/2505.18454",  # Hybrid Latent Reasoning via Reinforcement Learning
    "https://arxiv.org/abs/2505.18472",  # ManiFeel: Benchmarking and Understanding Visuotactile Manipulation Policy Learning
    "https://arxiv.org/abs/2505.18474",  # Canonical Policy: Learning Canonical 3D Representation for SE(3)-Equivariant Policy
    "https://arxiv.org/abs/2505.18499",  # G1: Teaching LLMs to Reason on Graphs with Reinforcement Learning
    "https://arxiv.org/abs/2505.18531",  # Generative RLHF-V: Learning Principles from Multi-modal Human Preference
    "https://arxiv.org/abs/2505.18547",  # Diffusion Blend: Inference-Time Multi-Preference Alignment for Diffusion Models
    "https://arxiv.org/abs/2505.18595",  # MisoDICE: Multi-Agent Imitation from Unlabeled Mixed-Quality Demonstrations
    "https://arxiv.org/abs/2505.18600",  # Chain-of-Zoom: Extreme Super-Resolution via Scale Autoregression and Preference Alignment
    "https://arxiv.org/abs/2505.18719",  # VLA-RL: Towards Masterful and General Robotic Manipulation with Scalable Reinforcement Learning
    "https://arxiv.org/abs/2505.18763",  # GenPO: Generative Diffusion Models Meet On-Policy Reinforcement Learning
    "https://arxiv.org/abs/2505.18830",  # On the Effect of Negative Gradient in Group Relative Deep Reinforcement Optimization
    "https://arxiv.org/abs/2505.18842",  # v1: Learning to Point Visual Tokens for Multimodal Grounded Reasoning
    "https://arxiv.org/abs/2505.18917",  # Behavior Injection: Preparing Language Models for Reinforcement Learning
    "https://arxiv.org/abs/2505.18947",  # OpenHOI: Open-World Hand-Object Interaction Synthesis with Multimodal Large Language Model
    "https://arxiv.org/abs/2505.18983",  # AmorLIP: Efficient Language-Image Pretraining via Amortization
    "https://arxiv.org/abs/2505.19000",  # VerIPO: Cultivating Long Reasoning in Video-LLMs via Verifier-Gudied Iterative Policy Optimization
    "https://arxiv.org/abs/2505.19017",  # WorldEval: World Model as Real-World Robot Policies Evaluator
    "https://arxiv.org/abs/2505.19030",  # RECAST: Expanding the Boundaries of LLMs' Complex Instruction Following with Multi-Constraint Data
    "https://arxiv.org/abs/2505.19053",  # Structured Reinforcement Learning for Combinatorial Decision-Making
    "https://arxiv.org/abs/2505.19092",  # Reinforced Latent Reasoning for LLM-based Recommendation
    "https://arxiv.org/abs/2505.19094",  # SATORI-R1: Incentivizing Multimodal Reasoning through Explicit Visual Anchoring
    "https://arxiv.org/abs/2505.19217",  # The Overthinker's DIET: Cutting Token Calories with DIfficulty-AwarE Training
    "https://arxiv.org/abs/2505.19223",  # LLaDA 1.5: Variance-Reduced Preference Optimization for Large Language Diffusion Models
    "https://arxiv.org/abs/2505.19255",  # VTool-R1: VLMs Learn to Think with Images via Reinforcement Learning on Multimodal Tool Use
    "https://arxiv.org/abs/2505.19281",  # A Snapshot of Influence: A Local Data Attribution Framework for Online Reinforcement Learning
    "https://arxiv.org/abs/2505.19386",  # Force Prompting: Video Generation Models Can Learn and Generalize Physics-based Control Signals
    "https://arxiv.org/abs/2505.19406",  # Unveiling the Compositional Ability Gap in Vision-Language Reasoning Model
    "https://arxiv.org/abs/2505.19486",  # VLMLight: Safety-Critical Traffic Signal Control via Vision-Language Meta-Control and Dual-Branch Reasoning Architecture
    "https://arxiv.org/abs/2505.19590",  # Learning to Reason without External Rewards
    "https://arxiv.org/abs/2505.19591",  # Multi-Agent Collaboration via Evolving Orchestration
    "https://arxiv.org/abs/2505.19641",  # SynLogic: Synthesizing Verifiable Reasoning Data at Scale for Learning Logical Reasoning and Beyond
    "https://arxiv.org/abs/2505.19702",  # Point-RFT: Improving Multimodal Reasoning with Visually Grounded Reinforcement Finetuning
    "https://arxiv.org/abs/2505.19707",  # MLLM-Guided VLM Fine-Tuning with Joint Inference for Zero-Shot Composed Image Retrieval
    "https://arxiv.org/abs/2505.19789",  # What Can RL Bring to VLA Generalization? An Empirical Study
    "https://arxiv.org/abs/2505.19850",  # DISCOVER: Automated Curricula for Sparse-Reward Reinforcement Learning
    "https://arxiv.org/abs/2505.19862",  # REA-RL: Reflection-Aware Online Reinforcement Learning for Efficient Reasoning
    "https://arxiv.org/abs/2505.19877",  # Vad-R1: Towards Video Anomaly Reasoning via Perception-to-Cognition Chain-of-Thought
    "https://arxiv.org/abs/2505.19914",  # Enigmata: Scaling Logical Reasoning in Large Language Models with Synthetic Verifiable Puzzles
    "https://arxiv.org/abs/2505.19985",  # Structured Initialization for Vision Transformers
    "https://arxiv.org/abs/2505.20046",  # REARANK: Reasoning Re-ranking Agent via Reinforcement Learning
    "https://arxiv.org/abs/2505.20065",  # SafeDPO: A Simple Approach to Direct Preference Optimization with Enhanced Safety
    "https://arxiv.org/abs/2505.20107",  # Refining Few-Step Text-to-Multiview Diffusion via Reinforcement Learning
    "https://arxiv.org/abs/2505.20131",  # MolEditRL: Structure-Preserving Molecular Editing via Discrete Diffusion and Reinforcement Learning
    "https://arxiv.org/abs/2505.20147",  # FUDOKI: Discrete Flow-based Unified Understanding and Generation via Kinetic-Optimal Velocities
    "https://arxiv.org/abs/2505.20164",  # Thinking with Visual Abstract: Enhancing Multimodal Reasoning via Visual Abstraction
    "https://arxiv.org/abs/2505.20229",  # From What to How: Attributing CLIP's Latent Components Reveals Unexpected Semantic Reliance
    "https://arxiv.org/abs/2505.20258",  # ARM: Adaptive Reasoning Model
    "https://arxiv.org/abs/2505.20268",  # Outcome-Based Online Reinforcement Learning: Algorithms and Fundamental Limits
    "https://arxiv.org/abs/2505.20279",  # VLM-3R: Vision-Language Models Augmented with Instruction-Aligned 3D Reconstruction
    "https://arxiv.org/abs/2505.20287",  # MotionPro: A Precise Motion Controller for Image-to-Video Generation
    "https://arxiv.org/abs/2505.20289",  # VisualToolAgent (VisTA): A Reinforcement Learning Framework for Visual Tool Selection
    "https://arxiv.org/abs/2505.20444",  # HoPE: Hybrid of Position Embedding for Long Context Vision-Language Models
    "https://arxiv.org/abs/2505.20561",  # Beyond Markovian: Reflective Exploration via Bayes-Adaptive RL for LLM Reasoning
    "https://arxiv.org/abs/2505.20612",  # Roboflow100-VL: A Multi-Domain Object Detection Benchmark for Vision-Language Models
    "https://arxiv.org/abs/2505.20686",  # Accelerating RL for LLM Reasoning with Optimal Advantage Regression
    "https://arxiv.org/abs/2505.20753",  # Understand, Think, and Answer: Advancing Visual Reasoning with Large Multimodal Models
    "https://arxiv.org/abs/2505.20793",  # Rendering-Aware Reinforcement Learning for Vector Graphics Generation
    "https://arxiv.org/abs/2505.20802",  # Leaner Transformers: More Heads, Less Depth
    "https://arxiv.org/abs/2505.20829",  # Learning a Unified Policy for Position and Force Control in Legged Loco-Manipulation
    "https://arxiv.org/abs/2505.20897",  # Cross from Left to Right Brain: Adaptive Text Dreamer for Vision-and-Language Navigation
    "https://arxiv.org/abs/2505.20922",  # Revisiting Multi-Agent World Modeling from a Diffusion-Inspired Perspective
    "https://arxiv.org/abs/2505.20948",  # Controllable Logical Hypothesis Generation for Abductive Reasoning in Knowledge Graphs
    "https://arxiv.org/abs/2505.21097",  # Thinker: Learning to Think Fast and Slow
    "https://arxiv.org/abs/2505.21119",  # Universal Value-Function Uncertainties
    "https://arxiv.org/abs/2505.21236",  # Breaking the Performance Ceiling in Reinforcement Learning requires Inference Strategies
    "https://arxiv.org/abs/2505.21391",  # Finite Sample Analysis of Linear Temporal Difference Learning with Arbitrary Features
    "https://arxiv.org/abs/2505.21444",  # Can Large Reasoning Models Self-Train?
    "https://arxiv.org/abs/2505.21457",  # Active-O3: Empowering Multimodal Large Language Models with Active Perception via GRPO
    "https://arxiv.org/abs/2505.21460",  # High-Dimensional Calibration from Swap Regret
    "https://arxiv.org/abs/2505.21465",  # ID-Align: RoPE-Conscious Position Remapping for Dynamic High-Resolution Adaptation in Vision-Language Models
    "https://arxiv.org/abs/2505.21478",  # Policy Optimized Text-to-Image Pipeline Design
    "https://arxiv.org/abs/2505.21493",  # Reinforcing General Reasoning without Verifiers
    "https://arxiv.org/abs/2505.21497",  # Paper2Poster: Towards Multimodal Poster Automation from Scientific Papers
    "https://arxiv.org/abs/2505.21500",  # ViewSpatial-Bench: Evaluating Multi-perspective Spatial Localization in Vision-Language Models
    "https://arxiv.org/abs/2505.21501",  # Vision Transformers with Self-Distilled Registers
    "https://arxiv.org/abs/2505.21533",  # Self-Organizing Visual Prototypes for Non-Parametric Representation Learning
    "https://arxiv.org/abs/2505.21538",  # Caption This, Reason That: VLMs Caught in the Middle
    "https://arxiv.org/abs/2505.21549",  # Distill CLIP (DCLIP): Enhancing Image-Text Retrieval via Cross-Modal Transformer Distillation
    "https://arxiv.org/abs/2505.21653",  # Think Before You Diffuse: Infusing Physical Rules into Video Diffusion
    "https://arxiv.org/abs/2505.21668",  # R1-Code-Interpreter: LLMs Reason with Code via Supervised and Multi-stage Reinforcement Learning
    "https://arxiv.org/abs/2505.21852",  # A Provable Approach for End-to-End Safe Reinforcement Learning
    "https://arxiv.org/abs/2505.21864",  # DexUMI: Using Human Hand as the Universal Manipulation Interface for Dexterous Manipulation
    "https://arxiv.org/abs/2505.21906",  # ChatVLA-2: Vision-Language-Action Model with Open-World Embodied Reasoning from Pretrained Knowledge
    "https://arxiv.org/abs/2505.21908",  # Reinforcement Learning for Out-of-Distribution Reasoning in LLMs: An Empirical Study on Diagnosis-Related Group Coding
    "https://arxiv.org/abs/2505.21996",  # Learning World Models for Interactive Video Generation
    "https://arxiv.org/abs/2505.22019",  # VRAG-RL: Empower Vision-Perception-Based RAG for Visually Rich Information Understanding via Iterative Reasoning with Reinforcement Learning
    "https://arxiv.org/abs/2505.22094",  # ReinFlow: Fine-tuning Flow Matching Policy with Online Reinforcement Learning
    "https://arxiv.org/abs/2505.22151",  # Oryx: a Scalable Sequence Model for Many-Agent Coordination in Offline MARL
    "https://arxiv.org/abs/2505.22159",  # ForceVLA: Enhancing VLA Models with a Force-aware MoE for Contact-rich Manipulation
    "https://arxiv.org/abs/2505.22195",  # S2AFormer: Strip Self-Attention for Efficient Vision Transformer
    "https://arxiv.org/abs/2505.22196",  # An Augmentation-Aware Theory for Self-Supervised Contrastive Learning
    "https://arxiv.org/abs/2505.22257",  # Revisiting Group Relative Policy Optimization: Insights into On-Policy and Off-Policy Training
    "https://arxiv.org/abs/2505.22323",  # Advancing Expert Specialization for Better MoE
    "https://arxiv.org/abs/2505.22334",  # Advancing Multimodal Reasoning via Reinforcement Learning with Cold Start
    "https://arxiv.org/abs/2505.22338",  # Text2Grad: Reinforcement Learning from Natural Language Feedback
    "https://arxiv.org/abs/2505.22453",  # First SFT, Second RL, Third UPT: Continual Improving Multi-Modal LLM Reasoning via Unsupervised Post-Training
    "https://arxiv.org/abs/2505.22525",  # Thinking with Generated Images
    "https://arxiv.org/abs/2505.22566",  # Universal Visuo-Tactile Video Understanding for Embodied Interaction
    "https://arxiv.org/abs/2505.22596",  # SAM-R1: Leveraging SAM for Reward Feedback in Multimodal Segmentation via Reinforcement Learning
    "https://arxiv.org/abs/2505.22617",  # The Entropy Mechanism of Reinforcement Learning for Reasoning Language Models
    "https://arxiv.org/abs/2505.22618",  # Fast-dLLM: Training-free Acceleration of Diffusion LLM by Enabling KV Cache and Parallel Decoding
    "https://arxiv.org/abs/2505.22642",  # FastTD3: Simple, Fast, and Capable Reinforcement Learning for Humanoid Control
    "https://arxiv.org/abs/2505.22648",  # WebDancer: Towards Autonomous Information Seeking Agency
    "https://arxiv.org/abs/2505.22651",  # Sherlock: Self-Correcting Reasoning in Vision-Language Models
    "https://arxiv.org/abs/2505.22654",  # VScan: Rethinking Visual Token Reduction for Efficient Large Vision-Language Models
    "https://arxiv.org/abs/2505.22664",  # Zero-Shot Vision Encoder Grafting via LLM Surrogates
    "https://arxiv.org/abs/2505.22704",  # Training Language Models to Generate Quality Code with Program Analysis Feedback
    "https://arxiv.org/abs/2505.22760",  # Non-convex entropic mean-field optimization via Best Response flow
    "https://arxiv.org/abs/2505.22866",  # Scaling Offline RL via Efficient and Expressive Shortcut Models
    "https://arxiv.org/abs/2505.22954",  # Darwin Godel Machine: Open-Ended Evolution of Self-Improving Agents
    "https://arxiv.org/abs/2505.23004",  # QLIP: A Dynamic Quadtree Vision Prior Enhances MLLM Performance Without Retraining
    "https://arxiv.org/abs/2505.23062",  # Composite Flow Matching for Reinforcement Learning with Shifted-Dynamics Data
    "https://arxiv.org/abs/2505.23131",  # DOPPLER: Dual-Policy Learning for Device Assignment in Asynchronous Dataflow Graphs
    "https://arxiv.org/abs/2505.23150",  # Bigger, Regularized, Categorical: High-Capacity Value Functions are Efficient Multi-Task Learners
    "https://arxiv.org/abs/2505.23224",  # MMBoundary: Advancing MLLM Knowledge Boundary Awareness through Reasoning Step Confidence Calibration
    "https://arxiv.org/abs/2505.23380",  # UniRL: Self-Improving Unified Multimodal Models via Supervised and Reinforcement Learning
    "https://arxiv.org/abs/2505.23387",  # Afterburner: Reinforcement Learning Facilitates Self-Improving Code Efficiency Optimization
    "https://arxiv.org/abs/2505.23416",  # KVzip: Query-Agnostic KV Cache Compression with Context Reconstruction
    "https://arxiv.org/abs/2505.23433",  # Diversity-Aware Policy Optimization for Large Language Model Reasoning
    "https://arxiv.org/abs/2505.23450",  # Agentic Robot: A Brain-Inspired Framework for Vision-Language-Action Models in Embodied Agents
    "https://arxiv.org/abs/2505.23527",  # Normalizing Flows are Capable Models for RL
    "https://arxiv.org/abs/2505.23579",  # BioReason: Incentivizing Multimodal Biological Reasoning within a DNA-LLM Model
    "https://arxiv.org/abs/2505.23585",  # On-Policy RL with Optimal Reward Baseline
    "https://arxiv.org/abs/2505.23590",  # Jigsaw-R1: A Study of Rule-based Visual Reinforcement Learning with Jigsaw Puzzles
    "https://arxiv.org/abs/2505.23614",  # Inference-time Scaling of Diffusion Models through Classical Search
    "https://arxiv.org/abs/2505.23653",  # How do Transformers Learn Implicit Reasoning?
    "https://arxiv.org/abs/2505.23656",  # VideoREPA: Learning Physics for Video Generation through Relational Alignment with Foundation Models
    "https://arxiv.org/abs/2505.23663",  # AMBER: Adaptive Mesh Generation by Iterative Mesh Resolution Prediction
    "https://arxiv.org/abs/2505.23678",  # Grounded Reinforcement Learning for Visual Reasoning
    "https://arxiv.org/abs/2505.23692",  # Mobi-$π$: Mobilizing Your Robot Learning Policy
    "https://arxiv.org/abs/2505.23705",  # Knowledge Insulating Vision-Language-Action Models: Train Fast, Run Fast, Generalize Better
    "https://arxiv.org/abs/2505.23725",  # MuLoCo: Muon is a practical inner optimizer for DiLoCo
    "https://arxiv.org/abs/2505.23727",  # PixelThink: Towards Efficient Chain-of-Pixel Reasoning
    "https://arxiv.org/abs/2505.23745",  # To Trust Or Not To Trust Your Vision-Language Model's Prediction
    "https://arxiv.org/abs/2505.23747",  # Spatial-MLLM: Boosting MLLM Capabilities in Visual-based Spatial Intelligence
    "https://arxiv.org/abs/2505.23764",  # MMSI-Bench: A Benchmark for Multi-Image Spatial Intelligence
    "https://arxiv.org/abs/2505.23766",  # Argus: Vision-Centric Reasoning with Grounded Chain-of-Thought
    "https://arxiv.org/abs/2505.23769",  # TextRegion: Text-Aligned Region Tokens from Frozen Image-Text Models
    "https://arxiv.org/abs/2505.23871",  # ADG: Ambient Diffusion-Guided Dataset Recovery for Corruption-Robust Offline Reinforcement Learning
    "https://arxiv.org/abs/2505.23885",  # OWL: Optimized Workforce Learning for General Multi-Agent Assistance in Real-World Task Automation
    "https://arxiv.org/abs/2505.24025",  # DINO-R1: Incentivizing Reasoning Capability in Vision Foundation Models
    "https://arxiv.org/abs/2505.24034",  # LlamaRL: A Distributed Asynchronous Reinforcement Learning Framework for Efficient Large-scale LLM Training
    "https://arxiv.org/abs/2505.24061",  # Measure gradients, not activations! Enhancing neuronal activity in deep reinforcement learning
    "https://arxiv.org/abs/2505.24068",  # DiffCoTune: Differentiable Co-Tuning for Cross-domain Robot Control
    "https://arxiv.org/abs/2505.24156",  # Towards a Generalizable Bimanual Foundation Policy via Flow-based Video Prediction
    "https://arxiv.org/abs/2505.24161",  # Proxy Target: Bridging the Gap Between Discrete Spiking Neural Networks and Continuous Control
    "https://arxiv.org/abs/2505.24182",  # Seeing is Not Reasoning: MVPBench for Graph-based Evaluation of Multi-path Visual Physical CoT
    "https://arxiv.org/abs/2505.24189",  # Fine-Tune an SLM or Prompt an LLM? The Case of Generating Low-Code Workflows
    "https://arxiv.org/abs/2505.24257",  # Out of Sight, Not Out of Context? Egocentric Spatial Reasoning in VLMs Across Disjoint Frames
    "https://arxiv.org/abs/2505.24332",  # DeepDiver: Adaptive Search Intensity Scaling via Open-Web Reinforcement Learning
    "https://arxiv.org/abs/2505.24541",  # Mixpert: Mitigating Multimodal Learning Conflicts with Efficient Mixture-of-Vision-Experts
    "https://arxiv.org/abs/2505.24630",  # Reasoning Models Hallucinate More: Factuality-Aware Reinforcement Learning for Large Reasoning Models
    "https://arxiv.org/abs/2505.24726",  # Reflect, Retry, Reward: Self-Improving LLMs via Reinforcement Learning
    "https://arxiv.org/abs/2505.24760",  # REASONING GYM: Reasoning Environments for Reinforcement Learning with Verifiable Rewards
    "https://arxiv.org/abs/2505.24864",  # ProRL: Prolonged Reinforcement Learning Expands Reasoning Boundaries in Large Language Models
    "https://arxiv.org/abs/2505.24872",  # ProxyThinker: Test-Time Guidance through Small Visual Reasoners
    "https://arxiv.org/abs/2506.00022",  # Scaling Physical Reasoning with the PHYSICS Dataset
    "https://arxiv.org/abs/2506.00070",  # Robot-R1: Reinforcement Learning for Enhanced Embodied Reasoning in Robotics
    "https://arxiv.org/abs/2506.00103",  # Writing-Zero: Bridge the Gap Between Non-verifiable Tasks and Verifiable Rewards
    "https://arxiv.org/abs/2506.00123",  # Visual Embodied Brain: Let Multimodal Large Language Models See, Think, and Control in Spaces
    "https://arxiv.org/abs/2506.00131",  # Belief-Based Offline Reinforcement Learning for Delay-Robust Policy Optimization
    "https://arxiv.org/abs/2506.00138",  # Intrinsic Goals for Autonomous Agents: Model-Based Exploration in Virtual Zebrafish Predicts Ethological Behavior and Whole-Brain Dynamics
    "https://arxiv.org/abs/2506.00318",  # Chain-of-Frames: Advancing Video Understanding in Multimodal LLMs via Frame-Aware Reasoning
    "https://arxiv.org/abs/2506.00467",  # SST: Self-training with Self-adaptive Thresholding for Semi-supervised Learning
    "https://arxiv.org/abs/2506.00513",  # SSAM: Self-Supervised Association Modeling for Test-Time Adaption
    "https://arxiv.org/abs/2506.00539",  # ARIA: Training Language Agents with Intention-Driven Reward Aggregation
    "https://arxiv.org/abs/2506.00613",  # WorldGym: World Model as An Environment for Policy Evaluation
    "https://arxiv.org/abs/2506.00895",  # State-Covering Trajectory Stitching for Diffusion Planners
    "https://arxiv.org/abs/2506.00917",  # Q-learning with Posterior Sampling
    "https://arxiv.org/abs/2506.01078",  # GThinker: Towards General Multimodal Reasoning via Cue-Guided Rethinking
    "https://arxiv.org/abs/2506.01097",  # Generic Token Compression in Multimodal Large Language Models from an Explainability Perspective
    "https://arxiv.org/abs/2506.01103",  # DeepVerse: 4D Autoregressive Video Generation as a World Model
    "https://arxiv.org/abs/2506.01167",  # Accelerated Learning with Linear Temporal Logic using Differentiable Simulation
    "https://arxiv.org/abs/2506.01183",  # Doubly Robust Alignment for Large Language Models
    "https://arxiv.org/abs/2506.01185",  # HoMeR: Learning In-the-Wild Mobile Manipulation via Hybrid Imitation and Whole-Body Control
    "https://arxiv.org/abs/2506.01247",  # Visual Sparse Steering: Improving Zero-shot Image Classification with Sparsity Guided Steering Vectors
    "https://arxiv.org/abs/2506.01299",  # Scalable In-Context Q-Learning
    "https://arxiv.org/abs/2506.01347",  # The Surprising Effectiveness of Negative Reinforcement in LLM Reasoning
    "https://arxiv.org/abs/2506.01369",  # Incentivizing LLMs to Self-Verify Their Answers
    "https://arxiv.org/abs/2506.01392",  # Sparse Imagination for Efficient Visual World Model Planning
    "https://arxiv.org/abs/2506.01393",  # Improved Regret Bounds for Gaussian Process Upper Confidence Bound in Bayesian Optimization
    "https://arxiv.org/abs/2506.01413",  # Incentivizing Reasoning for Advanced Instruction-Following of Large Language Models
    "https://arxiv.org/abs/2506.01597",  # Policy Newton Algorithm in Reproducing Kernel Hilbert Space
    "https://arxiv.org/abs/2506.01622",  # General agents contain world models
    "https://arxiv.org/abs/2506.01663",  # Zoom-Refine: Boosting High-Resolution Multimodal Understanding via Localized Zoom and Self-Refinement
    "https://arxiv.org/abs/2506.01713",  # SRPO: Enhancing Multimodal LLM Reasoning via Reflection-Aware Reinforcement Learning
    "https://arxiv.org/abs/2506.01716",  # Self-Challenging Language Model Agents
    "https://arxiv.org/abs/2506.01724",  # Active Learning via Vision-Language Model Adaptation with Open Data
    "https://arxiv.org/abs/2506.01783",  # Harnessing Chain-of-Thought Reasoning in Multimodal Large Language Models for Face Anti-Spoofing
    "https://arxiv.org/abs/2506.01844",  # SmolVLA: A Vision-Language-Action Model for Affordable and Efficient Robotics
    "https://arxiv.org/abs/2506.01850",  # MoDA: Modulation Adapter for Fine-Grained Visual Grounding in Instructional MLLMs
    "https://arxiv.org/abs/2506.01939",  # Beyond the 80/20 Rule: High-Entropy Minority Tokens Drive Effective Reinforcement Learning for LLM Reasoning
    "https://arxiv.org/abs/2506.02095",  # Cycle Consistency as Reward: Learning Image-Text Alignment without Human Preferences
    "https://arxiv.org/abs/2506.02096",  # SynthRL: Scaling Visual Reasoning with Verifiable Data Synthesis
    "https://arxiv.org/abs/2506.02126",  # Knowledge or Reasoning? A Close Look at How LLMs Think Across Domains
    "https://arxiv.org/abs/2506.02138",  # Revisiting LRP: Positional Attribution as the Missing Ingredient for Transformer Explainability
    "https://arxiv.org/abs/2506.02153",  # Small Language Models are the Future of Agentic AI
    "https://arxiv.org/abs/2506.02177",  # Act Only When It Pays: Efficient Reinforcement Learning for LLM Reasoning via Selective Rollouts
    "https://arxiv.org/abs/2506.02244",  # Physics-Guided Motion Loss for Video Generation Model
    "https://arxiv.org/abs/2506.02359",  # Auto-Labeling Data for Object Detection
    "https://arxiv.org/abs/2506.02385",  # Multi-agent Markov Entanglement
    "https://arxiv.org/abs/2506.02489",  # Grasp2Grasp: Vision-Based Dexterous Grasp Translation via Schrödinger Bridges
    "https://arxiv.org/abs/2506.02557",  # Kernel-based Unsupervised Embedding Alignment for Enhanced Visual Representation in Vision-language Models
    "https://arxiv.org/abs/2506.02794",  # PhysGaia: A Physics-Aware Benchmark with Multi-Body Interactions for Dynamic Novel View Synthesis
    "https://arxiv.org/abs/2506.02843",  # Random Registers for Cross-Domain Few-Shot Learning
    "https://arxiv.org/abs/2506.03079",  # ORV: 4D Occupancy-centric Robot Video Generation
    "https://arxiv.org/abs/2506.03096",  # FuseLIP: Multimodal Embeddings via Early Fusion of Discrete Tokens
    "https://arxiv.org/abs/2506.03135",  # OmniSpatial: Towards Comprehensive Spatial Reasoning Benchmark for Vision Language Models
    "https://arxiv.org/abs/2506.03141",  # Context as Memory: Scene-Consistent Interactive Long Video Generation with Memory Retrieval
    "https://arxiv.org/abs/2506.03147",  # UniWorld-V1: High-Resolution Semantic Encoders for Unified Visual Understanding and Generation
    "https://arxiv.org/abs/2506.03150",  # IllumiCraft: Unified Geometry and Illumination Diffusion for Controllable Video Generation
    "https://arxiv.org/abs/2506.03195",  # Unlabeled Data Improves Fine-Grained Image Zero-shot Classification with Multimodal LLMs
    "https://arxiv.org/abs/2506.03295",  # Unleashing the Reasoning Potential of Pre-trained LLMs by Critique Fine-Tuning on One Problem
    "https://arxiv.org/abs/2506.03340",  # Seeing the Arrow of Time in Large Multimodal Models
    "https://arxiv.org/abs/2506.03350",  # Adversarial Attacks on Robotic Vision Language Action Models
    "https://arxiv.org/abs/2506.03525",  # Video-Skill-CoT: Skill-based Chain-of-Thoughts for Domain-Adaptive Video Reasoning
    "https://arxiv.org/abs/2506.03569",  # MiMo-VL Technical Report
    "https://arxiv.org/abs/2506.03596",  # ControlThinker: Unveiling Latent Semantics for Controllable Image Generation through Visual Reasoning
    "https://arxiv.org/abs/2506.03637",  # RewardAnything: Generalizable Principle-Following Reward Models
    "https://arxiv.org/abs/2506.03642",  # Spatial Understanding from Videos: Structured Prompts Meet Simulation Data
    "https://arxiv.org/abs/2506.03719",  # On the Closed-Form of Flow Matching: Generalization Does Not Arise from Target Stochasticity
    "https://arxiv.org/abs/2506.04005",  # Vocabulary-free few-shot learning for Vision-Language Models
    "https://arxiv.org/abs/2506.04120",  # Splatting Physical Scenes: End-to-End Real-to-Sim from Imperfect Robot Data
    "https://arxiv.org/abs/2506.04171",  # Physics-Constrained Flow Matching: Sampling Generative Models with Hard Constraints
    "https://arxiv.org/abs/2506.04195",  # MACS: Multi-Agent Reinforcement Learning for Optimization of Crystal Structures
    "https://arxiv.org/abs/2506.04207",  # Advancing Multimodal Reasoning: From Optimized Cold Start to Staged Reinforcement Learning
    "https://arxiv.org/abs/2506.04209",  # Language-Image Alignment with Fixed Text Encoders
    "https://arxiv.org/abs/2506.04220",  # Struct2D: A Perception-Guided Framework for Spatial Reasoning in MLLMs
    "https://arxiv.org/abs/2506.04245",  # Contextual Integrity in LLMs via Reasoning and Reinforcement Learning
    "https://arxiv.org/abs/2506.04277",  # RSVP: Reasoning Segmentation via Visual Prompting and Multi-modal Chain-of-Thought
    "https://arxiv.org/abs/2506.04374",  # A Statistical Physics of Language Model Reasoning
    "https://arxiv.org/abs/2506.04398",  # Bridging the Performance Gap Between Target-Free and Target-Based Reinforcement Learning
    "https://arxiv.org/abs/2506.04411",  # Self-Supervised Contrastive Learning is Approximately Supervised Contrastive Learning
    "https://arxiv.org/abs/2506.04559",  # Reasoning-Aligned Perception Decoupling for Scalable Multi-modal Reasoning
    "https://arxiv.org/abs/2506.04632",  # Risk-Sensitive Agent Compositions
    "https://arxiv.org/abs/2506.04633",  # Unfolding Spatial Cognition: Evaluating Multimodal Models on Visual Simulations
    "https://arxiv.org/abs/2506.04695",  # Reshaping Reasoning in LLMs: A Theoretical Analysis of RL Training Dynamics through Pattern Selection
    "https://arxiv.org/abs/2506.04713",  # Enabling Validation for Robust Few-Shot Recognition
    "https://arxiv.org/abs/2506.04723",  # Beyond Accuracy: Dissecting Mathematical Reasoning for LLMs Under Reinforcement Learning
    "https://arxiv.org/abs/2506.04941",  # ArtVIP: Articulated Digital Assets of Visual Realism, Modular Interaction, and Physical Fidelity for Robot Learning
    "https://arxiv.org/abs/2506.05191",  # MokA: Multimodal Low-Rank Adaptation for MLLMs
    "https://arxiv.org/abs/2506.05259",  # Learning long range dependencies through time reversal symmetry breaking
    "https://arxiv.org/abs/2506.05284",  # Video World Models with Long-term Spatial Memory
    "https://arxiv.org/abs/2506.05302",  # Perceive Anything: Recognize, Explain, Caption, and Segment Anything in Images and Videos
    "https://arxiv.org/abs/2506.05316",  # Improving Data Efficiency for LLM Reinforcement Fine-tuning Through Difficulty-targeted Online Data Selection and Rollout Replay
    "https://arxiv.org/abs/2506.05340",  # Exploring Diffusion Transformer Designs via Grafting
    "https://arxiv.org/abs/2506.05426",  # Mixture-of-Experts Meets In-Context Reinforcement Learning
    "https://arxiv.org/abs/2506.05454",  # Zeroth-Order Optimization Finds Flat Minima
    "https://arxiv.org/abs/2506.05634",  # AutoQD: Automatic Discovery of Diverse Behaviors with Quality-Diversity Optimization
    "https://arxiv.org/abs/2506.05980",  # AMPED: Adaptive Multi-objective Projection for balancing Exploration and skill Diversification
    "https://arxiv.org/abs/2506.05997",  # Spatially-Enhanced Recurrent Memory for Long-Range Mapless Navigation via End-to-End Reinforcement Learning
    "https://arxiv.org/abs/2506.06105",  # Text-to-LoRA: Instant Transformer Adaption
    "https://arxiv.org/abs/2506.06122",  # Reinforcement Learning Optimization for Large-Scale Learning: An Efficient and User-Friendly Scaling Library
    "https://arxiv.org/abs/2506.06199",  # 3DFlowAction: Learning Cross-Embodiment Manipulation from 3D Flow World Model
    "https://arxiv.org/abs/2506.06259",  # An Optimized Franz-Parisi Criterion and its Equivalence with SQ Lower Bounds
    "https://arxiv.org/abs/2506.06279",  # CoMemo: LVLMs Need Image Context with Image Memory
    "https://arxiv.org/abs/2506.06303",  # Reward Is Enough: LLMs Are In-Context Reinforcement Learners
    "https://arxiv.org/abs/2506.06440",  # Vid2Sim: Generalizable, Video-based Reconstruction of Appearance, Geometry and Physics for Mesh-free Simulation
    "https://arxiv.org/abs/2506.06499",  # SPARQ: Synthetic Problem Generation for Reasoning via Quality-Diversity Algorithms
    "https://arxiv.org/abs/2506.06632",  # Curriculum Reinforcement Learning from Easy to Hard Tasks Improves LLM Reasoning
    "https://arxiv.org/abs/2506.06658",  # Self-Improving Loops for Visual Robotic Planning
    "https://arxiv.org/abs/2506.06677",  # RoboCerebra: A Large-scale Benchmark for Long-horizon Robotic Manipulation Evaluation
    "https://arxiv.org/abs/2506.06964",  # Offline RL by Reward-Weighted Fine-Tuning for Conversation Optimization
    "https://arxiv.org/abs/2506.06970",  # Guiding Cross-Modal Representations with MLLM Priors via Preference Alignment
    "https://arxiv.org/abs/2506.06981",  # Deep RL Needs Deep Behavior Analysis: Exploring Implicit Planning by Model-Free Agents in Open-Ended Environments
    "https://arxiv.org/abs/2506.07006",  # CARoL: Context-aware Adaptation for Robot Learning
    "https://arxiv.org/abs/2506.07047",  # Mathesis: Towards Formal Theorem Proving from Natural Languages
    "https://arxiv.org/abs/2506.07085",  # State Entropy Regularization for Robust Reinforcement Learning
    "https://arxiv.org/abs/2506.07127",  # Human-assisted Robotic Policy Refinement via Action Preference Optimization
    "https://arxiv.org/abs/2506.07138",  # Learning Compact Vision Tokens for Efficient Large Multimodal Models
    "https://arxiv.org/abs/2506.07218",  # Perception-R1: Advancing Multimodal Reasoning Capabilities of MLLMs via Visual Perception Reward
    "https://arxiv.org/abs/2506.07227",  # Hallucination at a Glance: Controlled Visual Edits and Fine-Grained Multimodal Learning
    "https://arxiv.org/abs/2506.07235",  # Multi-Step Visual Reasoning with Visual Tokens Scaling and Verification
    "https://arxiv.org/abs/2506.07254",  # A Stable Whitening Optimizer for Efficient Neural Network Training
    "https://arxiv.org/abs/2506.07259",  # ALINE: Joint Amortization for Bayesian Inference and Active Data Acquisition
    "https://arxiv.org/abs/2506.07326",  # Reward Model Interpretability via Optimal and Pessimal Tokens
    "https://arxiv.org/abs/2506.07339",  # Real-Time Execution of Action Chunking Flow Policies
    "https://arxiv.org/abs/2506.07413",  # Variational Supervised Contrastive Learning
    "https://arxiv.org/abs/2506.07468",  # Chasing Moving Targets with Online Self-Play Reinforcement Learning for Safer Language Models
    "https://arxiv.org/abs/2506.07527",  # Learning What Reinforcement Learning Can't: Interleaved Online Fine-Tuning for Hardest Questions
    "https://arxiv.org/abs/2506.07751",  # AbstRaL: Augmenting LLMs' Reasoning by Reinforcing Abstract Thinking
    "https://arxiv.org/abs/2506.07822",  # Accelerating Diffusion Planners in Offline RL via Reward-Aware Consistency Trajectory Distillation
    "https://arxiv.org/abs/2506.07850",  # SAM2Auto: Auto Annotation Using FLASH
    "https://arxiv.org/abs/2506.07936",  # Mimicking or Reasoning: Rethinking Multi-Modal In-Context Learning in Vision-Language Models
    "https://arxiv.org/abs/2506.07961",  # BridgeVLA: Input-Output Alignment for Efficient 3D Manipulation Learning with Vision-Language Models
    "https://arxiv.org/abs/2506.07966",  # SpaCE-10: A Comprehensive Benchmark for Multimodal Large Language Models in Compositional Spatial Intelligence
    "https://arxiv.org/abs/2506.08006",  # Dreamland: Controllable World Creation with Simulator and Generative Models
    "https://arxiv.org/abs/2506.08007",  # Reinforcement Pre-Training
    "https://arxiv.org/abs/2506.08008",  # Hidden in plain sight: VLMs overlook their visual representations
    "https://arxiv.org/abs/2506.08011",  # Play to Generalize: Learning to Reason Through Game Play
    "https://arxiv.org/abs/2506.08052",  # ReCogDrive: A Reinforced Cognitive Framework for End-to-End Autonomous Driving
    "https://arxiv.org/abs/2506.08062",  # FairDICE: Fairness-Driven Offline Multi-Objective Reinforcement Learning
    "https://arxiv.org/abs/2506.08257",  # Highly Compressed Tokenizer Can Generate Without Training
    "https://arxiv.org/abs/2506.08334",  # iTACO: Interactable Digital Twins of Articulated Objects from Casually Captured RGBD Videos
    "https://arxiv.org/abs/2506.08388",  # Reinforcement Learning Teachers of Test Time Scaling
    "https://arxiv.org/abs/2506.08391",  # SECOND: Mitigating Perceptual Hallucination in Vision-Language Models via Selective and Contrastive Decoding
    "https://arxiv.org/abs/2506.08429",  # Better Reasoning with Less Data: Enhancing VLMs Through Unified Modality Scoring
    "https://arxiv.org/abs/2506.08440",  # TGRPO :Fine-tuning Vision-Language-Action Model via Trajectory-wise Group Relative Policy Optimization
    "https://arxiv.org/abs/2506.08460",  # MOBODY: Model Based Off-Dynamics Offline Reinforcement Learning
    "https://arxiv.org/abs/2506.08552",  # Efficient Post-Training Refinement of Latent Reasoning in Large Language Models
    "https://arxiv.org/abs/2506.08672",  # RuleReasoner: Reinforced Rule-based Reasoning via Domain-aware Dynamic Sampling
    "https://arxiv.org/abs/2506.08681",  # Mitigating Reward Over-optimization in Direct Alignment Algorithms with Importance Sampling
    "https://arxiv.org/abs/2506.08708",  # PhyBlock: A Progressive Benchmark for Physical Understanding and Planning via 3D Block Assembly
    "https://arxiv.org/abs/2506.08745",  # Consistent Paths Lead to Truth: Self-Rewarding Reinforcement Learning for LLM Reasoning
    "https://arxiv.org/abs/2506.08822",  # FreqPolicy: Efficient Flow-based Visuomotor Policy via Frequency Consistency
    "https://arxiv.org/abs/2506.08898",  # Preference-Driven Multi-Objective Combinatorial Optimization with Conditional Computation
    "https://arxiv.org/abs/2506.08902",  # Intention-Conditioned Flow Occupancy Models
    "https://arxiv.org/abs/2506.08989",  # SwS: Self-aware Weakness-driven Problem Synthesis in Reinforcement Learning for LLM Reasoning
    "https://arxiv.org/abs/2506.09026",  # e3: Learning to Explore Enables Extrapolation of Test-Time Compute for LLMs
    "https://arxiv.org/abs/2506.09033",  # Router-R1: Teaching LLMs Multi-Round Routing and Aggregation via Reinforcement Learning
    "https://arxiv.org/abs/2506.09047",  # Same Task, Different Circuits: Disentangling Modality-Specific Mechanisms in VLMs
    "https://arxiv.org/abs/2506.09079",  # VidBridge-R1: Bridging QA and Captioning for RL-based Video Understanding Models with Intermediate Proxy Tasks
    "https://arxiv.org/abs/2506.09278",  # UFM: A Simple Path towards Unified Dense Correspondence with Flow
    "https://arxiv.org/abs/2506.09366",  # SkillBlender: Towards Versatile Humanoid Whole-Body Loco-Manipulation via Skill Blending
    "https://arxiv.org/abs/2506.09434",  # When Is Diversity Rewarded in Cooperative Multi-Agent Learning?
    "https://arxiv.org/abs/2506.09477",  # On a few pitfalls in KL divergence gradient estimation for RL
    "https://arxiv.org/abs/2506.09501",  # Understanding and Mitigating Numerical Sources of Nondeterminism in LLM Inference
    "https://arxiv.org/abs/2506.09508",  # Efficient Preference-Based Reinforcement Learning: Randomized Exploration Meets Experimental Design
    "https://arxiv.org/abs/2506.09522",  # Revisit What You See: Disclose Language Prior in Vision Tokens for LVLM Decoding
    "https://arxiv.org/abs/2506.09691",  # Adding simple structure at inference improves Vision-Language Compositionality
    "https://arxiv.org/abs/2506.09714",  # Auto-Compressing Networks
    "https://arxiv.org/abs/2506.09820",  # CoRT: Code-integrated Reasoning within Thinking
    "https://arxiv.org/abs/2506.09839",  # OctoNav: Towards Generalist Embodied Navigation
    "https://arxiv.org/abs/2506.09849",  # IntPhys 2: Benchmarking Intuitive Physics Understanding In Complex Synthetic Environments
    "https://arxiv.org/abs/2506.09937",  # SAFE: Multitask Failure Detection for Vision-Language-Action Models
    "https://arxiv.org/abs/2506.09943",  # CausalVQA: A Physically Grounded Causal Reasoning Benchmark for Video Models
    "https://arxiv.org/abs/2506.09965",  # Reinforcing Spatial Reasoning in Vision-Language Models with Interwoven Thinking and Visual Drawing
    "https://arxiv.org/abs/2506.09967",  # Resa: Transparent Reasoning Models via SAEs
    "https://arxiv.org/abs/2506.09985",  # V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning
    "https://arxiv.org/abs/2506.09987",  # A Shortcut-aware Video-QA Benchmark for Physical Understanding via Minimal Video Pairs
    "https://arxiv.org/abs/2506.09995",  # PlayerOne: Egocentric World Simulator
    "https://arxiv.org/abs/2506.10047",  # GenBreak: Red Teaming Text-to-Image Generators Using Large Language Models
    "https://arxiv.org/abs/2506.10054",  # Uni-DPO: A Unified Paradigm for Dynamic Preference Optimization of LLMs
    "https://arxiv.org/abs/2506.10085",  # VITA: Zero-Shot Value Functions via Test-Time Adaptation of Vision-Language Models
    "https://arxiv.org/abs/2506.10100",  # EfficientVLA: Training-Free Acceleration and Compression for Vision-Language-Action Models
    "https://arxiv.org/abs/2506.10128",  # ViCrit: A Verifiable Reinforcement Learning Proxy Task for Visual Perception in VLMs
    "https://arxiv.org/abs/2506.10133",  # Statistical Guarantees for Offline Domain Randomization
    "https://arxiv.org/abs/2506.10138",  # Path Channels and Plan Extension Kernels: a Mechanistic Description of Planning in a Sokoban RNN
    "https://arxiv.org/abs/2506.10139",  # Unsupervised Elicitation of Language Models
    "https://arxiv.org/abs/2506.10159",  # Probabilistic Variational Contrastive Learning
    "https://arxiv.org/abs/2506.10353",  # Motion-R1: Enhancing Motion Generation with Decomposed Chain-of-Thought and RL Binding
    "https://arxiv.org/abs/2506.10741",  # PosterCraft: Rethinking High-Quality Aesthetic Poster Generation in a Unified Framework
    "https://arxiv.org/abs/2506.10778",  # SlotPi: Physics-informed Object-centric Reasoning Models
    "https://arxiv.org/abs/2506.10910",  # Magistral
    "https://arxiv.org/abs/2506.10943",  # Self-Adapting Language Models
    "https://arxiv.org/abs/2506.10947",  # Spurious Rewards: Rethinking Training Signals in RLVR
    "https://arxiv.org/abs/2506.10966",  # GENMANIP: LLM-driven Simulation for Generalizable Instruction-Following Manipulation
    "https://arxiv.org/abs/2506.10967",  # Beyond Attention or Similarity: Maximizing Conditional Diversity for Token Pruning in MLLMs
    "https://arxiv.org/abs/2506.10975",  # GenWorld: Towards Detecting AI-generated Real-world Simulation Videos
    "https://arxiv.org/abs/2506.10979",  # How Well Can Reasoning Models Identify and Recover from Unhelpful Thoughts?
    "https://arxiv.org/abs/2506.11033",  # Adaptive Shielding for Safe Reinforcement Learning under Hidden-Parameter Dynamics Shifts
    "https://arxiv.org/abs/2506.11136",  # JAFAR: Jack up Any Feature at Any Resolution
    "https://arxiv.org/abs/2506.11442",  # ReVeal: Self-Evolving Code Agents via Reliable Self-Verification
    "https://arxiv.org/abs/2506.11487",  # Reviving DSP for Advanced Theorem Proving in the Era of Reasoning Models
    "https://arxiv.org/abs/2506.11515",  # Manager: Aggregating Insights from Unimodal Experts in Two-Tower VLMs and MLLMs
    "https://arxiv.org/abs/2506.11902",  # TreeRL: LLM Reinforcement Learning with On-Policy Tree Search
    "https://arxiv.org/abs/2506.11967",  # Visual Pre-Training on Unlabeled Images using Reinforcement Learning
    "https://arxiv.org/abs/2506.11976",  # How Visual Representations Map to Language Feature Space in Multimodal LLMs
    "https://arxiv.org/abs/2506.11991",  # VGR: Visual Grounded Reasoning
    "https://arxiv.org/abs/2506.12115",  # Eliciting Reasoning in Language Models with Cognitive Tools
    "https://arxiv.org/abs/2506.12508",  # AgentOrchestra: Orchestrating Multi-Agent Intelligence with the Tool-Environment-Agent(TEA) Protocol
    "https://arxiv.org/abs/2506.12609",  # Not All Tokens and Heads Are Equally Important: Dual-Level Attention Intervention for Hallucination Mitigation
    "https://arxiv.org/abs/2506.12622",  # DR-SAC: Distributionally Robust Soft Actor-Critic for Reinforcement Learning under Uncertainty
    "https://arxiv.org/abs/2506.12698",  # Unsupervised Contrastive Learning Using Out-Of-Distribution Data for Long-Tailed Dataset
    "https://arxiv.org/abs/2506.12723",  # SP-VLA: A Joint Model Scheduling and Token Pruning Approach for VLA Model Acceleration
    "https://arxiv.org/abs/2506.12776",  # Native Visual Understanding: Resolving Resolution Dilemmas in Vision-Language Models
    "https://arxiv.org/abs/2506.12779",  # From Experts to a Generalist: Toward General Whole-Body Control for Humanoid Robots
    "https://arxiv.org/abs/2506.12811",  # Flow-Based Policy for Online Reinforcement Learning
    "https://arxiv.org/abs/2506.12815",  # TrojanTO: Action-Level Backdoor Attacks against Trajectory Optimization Models
    "https://arxiv.org/abs/2506.12851",  # KungfuBot: Physics-Based Humanoid Whole-Body Control for Learning Highly-Dynamic Skills
    "https://arxiv.org/abs/2506.12932",  # Complexity Scaling Laws for Neural Models using Combinatorial Optimization
    "https://arxiv.org/abs/2506.13018",  # Symmetry in Neural Network Parameter Spaces
    "https://arxiv.org/abs/2506.13040",  # MAMMA: Markerless & Automatic Multi-Person Motion Action Capture
    "https://arxiv.org/abs/2506.13056",  # Metis-RISE: RL Incentivizes and SFT Enhances Multimodal Reasoning Model Learning
    "https://arxiv.org/abs/2506.13131",  # AlphaEvolve: A coding agent for scientific and algorithmic discovery
    "https://arxiv.org/abs/2506.13284",  # AceReason-Nemotron 1.1: Advancing Math and Code Reasoning through SFT and RL Synergy
    "https://arxiv.org/abs/2506.13331",  # Mixture of Cognitive Reasoners: Modular Reasoning with Brain-Like Specialization
    "https://arxiv.org/abs/2506.13351",  # Direct Reasoning Optimization: Constrained RL with Token-Level Dense Reward and Rubric-Gated Constraints for Open-ended Tasks
    "https://arxiv.org/abs/2506.13456",  # Block-wise Adaptive Caching for Accelerating Diffusion Policy
    "https://arxiv.org/abs/2506.13585",  # MiniMax-M1: Scaling Test-Time Compute Efficiently with Lightning Attention
    "https://arxiv.org/abs/2506.13690",  # Meta-learning how to Share Credit among Macro-Actions
    "https://arxiv.org/abs/2506.13723",  # OTFusion: Bridging Vision-only and Vision-Language Models via Optimal Transport for Transductive Zero-Shot Learning
    "https://arxiv.org/abs/2506.13751",  # LeVERB: Humanoid Whole-Body Control with Latent Vision-Language Instruction
    "https://arxiv.org/abs/2506.13757",  # AutoVLA: A Vision-Language-Action Model for End-to-End Autonomous Driving with Adaptive Reasoning and Reinforcement Fine-Tuning
    "https://arxiv.org/abs/2506.13759",  # Discrete Diffusion in Large Language and Multimodal Models: A Survey
    "https://arxiv.org/abs/2506.13888",  # VL-GenRM: Enhancing Vision-Language Verification via Vision Experts and Iterative Training
    "https://arxiv.org/abs/2506.13923",  # Adaptive Guidance Accelerates Reinforcement Learning of Reasoning Models
    "https://arxiv.org/abs/2506.13925",  # Segmenting Visuals With Querying Words: Language Anchors For Semi-Supervised Image Segmentation
    "https://arxiv.org/abs/2506.14135",  # GAF: Gaussian Action Field as a 4D Representation for Dynamic World Modeling in Robotic Manipulation
    "https://arxiv.org/abs/2506.14245",  # Reinforcement Learning with Verifiable Rewards Implicitly Incentivizes Correct Reasoning in Base LLMs
    "https://arxiv.org/abs/2506.14512",  # SIRI-Bench: Challenging VLMs' Spatial Intelligence through Complex Reasoning Tasks
    "https://arxiv.org/abs/2506.14608",  # Latent Action Diffusion for Cross-Embodiment Manipulation
    "https://arxiv.org/abs/2506.14641",  # Revisiting Chain-of-Thought Prompting: Zero-shot Can Be Stronger than Few-shot
    "https://arxiv.org/abs/2506.14728",  # AgentDistill: Training-Free Agent Distillation with Generalizable MCP Boxes
    "https://arxiv.org/abs/2506.14754",  # Tactile Beyond Pixels: Multisensory Touch Representations for Robot Manipulation
    "https://arxiv.org/abs/2506.14907",  # PeRL: Permutation-Enhanced Reinforcement Learning for Interleaved Vision-Language Reasoning
    "https://arxiv.org/abs/2506.14965",  # Revisiting Reinforcement Learning for LLM Reasoning from A Cross-Domain Perspective
    "https://arxiv.org/abs/2506.14968",  # FEAST: A Flexible Mealtime-Assistance System Towards In-the-Wild Personalization
    "https://arxiv.org/abs/2506.15050",  # Truncated Proximal Policy Optimization
    "https://arxiv.org/abs/2506.15211",  # ProtoReasoning: Prototypes as the Foundation for Generalizable Reasoning in LLMs
    "https://arxiv.org/abs/2506.15544",  # Stable Gradients for Stable Learning at Scale in Deep Reinforcement Learning
    "https://arxiv.org/abs/2506.15564",  # Show-o2: Improved Native Unified Multimodal Models
    "https://arxiv.org/abs/2506.15666",  # Vision in Action: Learning Active Perception from Human Demonstrations
    "https://arxiv.org/abs/2506.15673",  # UniRelight: Learning Joint Decomposition and Synthesis for Video Relighting
    "https://arxiv.org/abs/2506.15679",  # Dense SAE Latents Are Features, Not Bugs
    "https://arxiv.org/abs/2506.15680",  # Particle-Grid Neural Dynamics for Learning Deformable Object Models from RGB-D Videos
    "https://arxiv.org/abs/2506.15692",  # MLE-STAR: Machine Learning Engineering Agent via Search and Targeted Refinement
    "https://arxiv.org/abs/2506.15701",  # Compiler-R1: Towards Agentic Compiler Auto-tuning with Reinforcement Learning
    "https://arxiv.org/abs/2506.15710",  # RAST: Reasoning Activation in LLMs via Small-model Transfer
    "https://arxiv.org/abs/2506.15757",  # Weakly-supervised VLM-guided Partial Contrastive Learning for Visual Language Navigation
    "https://arxiv.org/abs/2506.15799",  # Steering Your Diffusion Policy with Latent Space Reinforcement Learning
    "https://arxiv.org/abs/2506.15841",  # MEM1: Learning to Synergize Memory and Reasoning for Efficient Long-Horizon Agents
    "https://arxiv.org/abs/2506.15953",  # ViTacFormer: Learning Cross-Modal Representation for Visuo-Tactile Dexterous Manipulation
    "https://arxiv.org/abs/2506.16012",  # DualTHOR: A Dual-Arm Humanoid Simulation Platform for Contingency-Aware Planning
    "https://arxiv.org/abs/2506.16016",  # Dual-Objective Reinforcement Learning with Novel Hamilton-Jacobi-Bellman Formulations
    "https://arxiv.org/abs/2506.16029",  # EvoLM: In Search of Lost Language Model Training Dynamics
    "https://arxiv.org/abs/2506.16112",  # Loss-Oriented Ranking for Automated Visual Prompting in LVLMs
    "https://arxiv.org/abs/2506.16141",  # GRPO-CARE: Consistency-Aware Reinforcement Learning for Multimodal Reasoning
    "https://arxiv.org/abs/2506.16396",  # GoalLadder: Incremental Goal Discovery with Vision-Language Models
    "https://arxiv.org/abs/2506.16590",  # Energy-Based Transfer for Reinforcement Learning
    "https://arxiv.org/abs/2506.16608",  # Distributions as Actions: A Unified Framework for Diverse Action Spaces
    "https://arxiv.org/abs/2506.16673",  # Extracting Multimodal Learngene in CLIP: Unveiling the Multimodal Generalizable Knowledge
    "https://arxiv.org/abs/2506.16691",  # LaVi: Efficient Large Vision-Language Models via Internal Feature Modulation
    "https://arxiv.org/abs/2506.16895",  # With Limited Data for Multimodal Alignment, Let the STRUCTURE Guide You
    "https://arxiv.org/abs/2506.17007",  # Discrete Compositional Generation via General Soft Operators and Robust Reinforcement Learning
    "https://arxiv.org/abs/2506.17093",  # Identifiability of Deep Polynomial Neural Networks
    "https://arxiv.org/abs/2506.17198",  # Dex1B: Learning with 1B Demonstrations for Dexterous Manipulation
    "https://arxiv.org/abs/2506.17202",  # UniFork: Exploring Modality Alignment for Unified Multimodal Understanding and Generation
    "https://arxiv.org/abs/2506.17218",  # Machine Mental Imagery: Empower Multimodal Reasoning with Latent Visual Tokens
    "https://arxiv.org/abs/2506.17219",  # No Free Lunch: Rethinking Internal Feedback for LLM Reasoning
    "https://arxiv.org/abs/2506.17238",  # Training a Scientific Reasoning Model for Chemistry
    "https://arxiv.org/abs/2506.17561",  # VLA-OS: Structuring and Dissecting Planning Representations and Paradigms in Vision-Language-Action Models
    "https://arxiv.org/abs/2506.17608",  # HIRE: Lightweight High-Resolution Image Feature Enrichment for Multimodal LLMs
    "https://arxiv.org/abs/2506.17629",  # CLiViS: Unleashing Cognitive Map through Linguistic-Visual Synergy for Embodied Visual Reasoning
    "https://arxiv.org/abs/2506.17639",  # RLRC: Reinforcement Learning-based Recovery for Compressed Vision-Language-Action Models
    "https://arxiv.org/abs/2506.17901",  # PostAlign: Multimodal Grounding as a Corrective Lens for MLLMs
    "https://arxiv.org/abs/2506.18088",  # RoboTwin 2.0: A Scalable Data Generator and Benchmark with Strong Domain Randomization for Robust Bimanual Robotic Manipulation
    "https://arxiv.org/abs/2506.18110",  # RL for Reasoning by Adaptively Revealing Rationales
    "https://arxiv.org/abs/2506.18123",  # RoboArena: Distributed Real-World Evaluation of Generalist Robot Policies
    "https://arxiv.org/abs/2506.18254",  # RLPR: Extrapolating RLVR to General Domains without Verifiers
    "https://arxiv.org/abs/2506.18369",  # RePIC: Reinforced Post-Training for Personalizing Multi-Modal Language Models
    "https://arxiv.org/abs/2506.18385",  # InternSpatial: A Comprehensive Dataset for Spatial Reasoning in Vision-Language Models
    "https://arxiv.org/abs/2506.18448",  # GraspMAS: Zero-Shot Language-driven Grasp Detection with Multi-Agent System
    "https://arxiv.org/abs/2506.18482",  # Reliability-Adjusted Prioritized Experience Replay
    "https://arxiv.org/abs/2506.18485",  # A Simple "Motivation" Can Enhance Reinforcement Finetuning of Large Reasoning Models
    "https://arxiv.org/abs/2506.18504",  # Generalizing vision-language models to novel domains: A comprehensive survey
    "https://arxiv.org/abs/2506.18655",  # RDPO: Real Data Preference Optimization for Physics Consistency Video Generation
    "https://arxiv.org/abs/2506.18701",  # Matrix-Game: Interactive World Foundation Model
    "https://arxiv.org/abs/2506.18841",  # LongWriter-Zero: Mastering Ultra-Long Text Generation via Reinforcement Learning
    "https://arxiv.org/abs/2506.18945",  # Chain-of-Experts: Unlocking the Communication Power of Mixture-of-Experts Models
    "https://arxiv.org/abs/2506.19212",  # Scaffolding Dexterous Manipulation with Vision-Language Models
    "https://arxiv.org/abs/2506.19360",  # SoK: Can Synthetic Images Replace Real Data? A Survey of Utility and Privacy of Synthetic Image Generation
    "https://arxiv.org/abs/2506.19699",  # UniTac-NV: A Unified Tactile Representation For Non-Vision-Based Tactile Sensors
    "https://arxiv.org/abs/2506.19733",  # Breaking Barriers: Do Reinforcement Post Training Gains Transfer To Unseen Domains?
    "https://arxiv.org/abs/2506.19767",  # SRFT: A Single-Stage Method with Supervised and Reinforcement Fine-Tuning for Reasoning
    "https://arxiv.org/abs/2506.19798",  # CoCo4D: Comprehensive and Complex 4D Scene Generation
    "https://arxiv.org/abs/2506.19807",  # KnowRL: Exploring Knowledgeable Reinforcement Learning for Factuality
    "https://arxiv.org/abs/2506.19816",  # CronusVLA: Towards Efficient and Robust Manipulation via Multi-Frame Vision-Language-Action Modeling
    "https://arxiv.org/abs/2506.19823",  # Persona Features Control Emergent Misalignment
    "https://arxiv.org/abs/2506.19850",  # Unified Vision-Language-Action Model
    "https://arxiv.org/abs/2506.19997",  # TRACED: Transition-aware Regret Approximation with Co-learnability for Environment Design
    "https://arxiv.org/abs/2506.20048",  # A Principled Path to Fitted Distributional Evaluation
    "https://arxiv.org/abs/2506.20134",  # From 2D to 3D Cognition: A Brief Survey of General World Models
    "https://arxiv.org/abs/2506.20168",  # Seeing is Believing? Mitigating OCR Hallucinations in Multimodal Large Language Models
    "https://arxiv.org/abs/2506.20553",  # Sim2Val: Leveraging Correlation Across Test Platforms for Variance-Reduced Metric Estimation
    "https://arxiv.org/abs/2506.20629",  # PLoP: Precise LoRA Placement for Efficient Finetuning of Large Models
    "https://arxiv.org/abs/2506.20639",  # DiffuCoder: Understanding and Improving Masked Diffusion Models for Code Generation
    "https://arxiv.org/abs/2506.20703",  # Generative Blocks World: Moving Things Around in Pictures
    "https://arxiv.org/abs/2506.20904",  # Optimal Single-Policy Sample Complexity and Transient Coverage for Average-Reward Offline RL
    "https://arxiv.org/abs/2506.20966",  # Parallels Between VLA Model Post-Training and Human Motor Learning: Progress, Challenges, and Trends
    "https://arxiv.org/abs/2506.21039",  # Strict Subgoal Execution: Reliable Long-Horizon Planning in Hierarchical Reinforcement Learning
    "https://arxiv.org/abs/2506.21046",  # Boosting Generative Adversarial Transferability with Self-supervised Vision Transformer Features
    "https://arxiv.org/abs/2506.21215",  # Unveiling Causal Reasoning in Large Language Models: Reality or Mirage?
    "https://arxiv.org/abs/2506.21427",  # Flow-Based Single-Step Completion for Efficient and Expressive Policy Learning
    "https://arxiv.org/abs/2506.21458",  # Spatial Mental Modeling from Limited Views
    "https://arxiv.org/abs/2506.21495",  # Bridging Offline and Online Reinforcement Learning for LLMs
    "https://arxiv.org/abs/2506.21539",  # WorldVLA: Towards Autoregressive Action World Model
    "https://arxiv.org/abs/2506.21656",  # Fine-Grained Preference Optimization Improves Spatial Reasoning in VLMs
    "https://arxiv.org/abs/2506.21669",  # SEEA-R1: Tree-Structured Reinforcement Fine-Tuning for Self-Evolving Embodied Agents
    "https://arxiv.org/abs/2506.21683",  # Risk-Averse Total-Reward Reinforcement Learning
    "https://arxiv.org/abs/2506.21710",  # FOCUS: Internal MLLM Representations for Efficient Fine-Grained Visual Question Answering
    "https://arxiv.org/abs/2506.21734",  # Hierarchical Reasoning Model
    "https://arxiv.org/abs/2506.21872",  # A Survey of Continual Reinforcement Learning
    "https://arxiv.org/abs/2506.22007",  # RoboEnvision: A Long-Horizon Video Generation Model for Multi-Task Robot Manipulation
    "https://arxiv.org/abs/2506.22242",  # 4D-VLA: Spatiotemporal Vision-Language-Action Pretraining with Cross-Scene Calibration
    "https://arxiv.org/abs/2506.22355",  # Embodied AI Agents: Modeling the World
    "https://arxiv.org/abs/2506.22395",  # Test-Time Consistency in Vision Language Models
    "https://arxiv.org/abs/2506.22401",  # Exploration from a Primal-Dual Lens: Value-Incentivized Actor-Critic Methods for Sample-Efficient Online RL
    "https://arxiv.org/abs/2506.22419",  # The Automated LLM Speedrunning Benchmark: Reproducing NanoGPT Improvements
    "https://arxiv.org/abs/2506.22434",  # MiCo: Multi-image Contrast for Reinforcement Visual Reasoning
    "https://arxiv.org/abs/2506.22624",  # Seg-R1: Segmentation Can Be Surprisingly Simple with Reinforcement Learning
    "https://arxiv.org/abs/2506.22712",  # Generalized Linear Mode Connectivity for Transformers
    "https://arxiv.org/abs/2506.22819",  # Prompting without Panic: Attribute-aware, Zero-shot, Test-Time Calibration
    "https://arxiv.org/abs/2506.22880",  # Decoupled Seg Tokens Make Stronger Reasoning Video Segmenter and Grounder
    "https://arxiv.org/abs/2506.22982",  # Revisiting CroPA: A Reproducibility Study and Enhancements for Cross-Prompt Adversarial Transferability in Vision-Language Models
    "https://arxiv.org/abs/2506.22992",  # MARBLE: A Hard Benchmark for Multimodal Spatial Reasoning and Planning
    "https://arxiv.org/abs/2506.23044",  # Ovis-U1 Technical Report
    "https://arxiv.org/abs/2506.23061",  # Empowering Small VLMs to Think with Dynamic Memorization and Exploration
    "https://arxiv.org/abs/2506.23114",  # Minimizing Acoustic Noise: Enhancing Quiet Locomotion for Quadruped Robots in Indoor Applications
    "https://arxiv.org/abs/2506.23115",  # MoCa: Modality-aware Continual Pre-training Makes Better Bidirectional Multimodal Embeddings
    "https://arxiv.org/abs/2506.23120",  # Enhancing Spatial Reasoning in Multimodal Large Language Models through Reasoning-based Segmentation
    "https://arxiv.org/abs/2506.23126",  # ParticleFormer: A 3D Point Cloud World Model for Multi-Object, Multi-Material Robotic Manipulation
    "https://arxiv.org/abs/2506.23135",  # RoboScape: Physics-informed Embodied World Model
    "https://arxiv.org/abs/2506.23156",  # Self-Supervised Contrastive Learning for Multi-Label Images
    "https://arxiv.org/abs/2506.23235",  # Generalist Reward Models: Found Inside Large Language Models
    "https://arxiv.org/abs/2506.23316",  # SceneStreamer: Continuous Scenario Generation as Next Token Group Prediction
    "https://arxiv.org/abs/2506.23468",  # NavMorph: A Self-Evolving World Model for Vision-and-Language Navigation in Continuous Environments
    "https://arxiv.org/abs/2506.23529",  # When Test-Time Adaptation Meets Self-Supervised Models
    "https://arxiv.org/abs/2506.23601",  # Semantic-guided Diverse Decoding for Large Language Model
    "https://arxiv.org/abs/2506.23639",  # Unified Multimodal Understanding via Byte-Pair Visual Encoding
    "https://arxiv.org/abs/2506.23785",  # Visual Textualization for Image Prompted Object Detection
    "https://arxiv.org/abs/2506.23822",  # Interpretable Zero-Shot Learning with Locally-Aligned Vision-Language Model
    "https://arxiv.org/abs/2506.23918",  # Thinking with Images for Multimodal Reasoning: Foundations, Methods, and Future Frontiers
    "https://arxiv.org/abs/2506.24119",  # SPIRAL: Self-Play on Zero-Sum Games Incentivizes Reasoning via Multi-Agent Multi-Turn Reinforcement Learning
    "https://arxiv.org/abs/2507.00416",  # Evo-0: Vision-Language-Action Model with Implicit Spatial Understanding
    "https://arxiv.org/abs/2507.00417",  # ASTRO: Teaching Language Models to Reason by Reflecting and Backtracking In-Context
    "https://arxiv.org/abs/2507.00432",  # Does Math Reasoning Improve General LLM Capabilities? Understanding Transferability of LLM Reasoning
    "https://arxiv.org/abs/2507.00435",  # RoboEval: Where Robotic Manipulation Meets Structured and Scalable Evaluation
    "https://arxiv.org/abs/2507.00462",  # Unleashing the Potential of All Test Samples: Mean-Shift Guided Test-Time Adaptation
    "https://arxiv.org/abs/2507.00505",  # LLaVA-SP: Enhancing Visual Representation with Visual Spatial Tokens for MLLMs
    "https://arxiv.org/abs/2507.00748",  # Improving the Reasoning of Multi-Image Grounding in MLLMs via Reinforcement Learning
    "https://arxiv.org/abs/2507.00754",  # Language-Unlocked ViT (LUViT): Empowering Self-Supervised Vision Transformers with LLMs
    "https://arxiv.org/abs/2507.00833",  # HumanoidGen: Data Generation for Bimanual Dexterous Manipulation via LLM Reasoning
    "https://arxiv.org/abs/2507.00898",  # ONLY: One-Layer Intervention Sufficiently Mitigates Hallucinations in Large Vision-Language Models
    "https://arxiv.org/abs/2507.00917",  # A Survey: Learning Embodied Intelligence from Physical Simulators and World Models
    "https://arxiv.org/abs/2507.00971",  # Reasoning as an Adaptive Defense for Safety
    "https://arxiv.org/abs/2507.00990",  # Robotic Manipulation by Imitating Generated Videos Without Physical Demonstrations
    "https://arxiv.org/abs/2507.00994",  # Should We Still Pretrain Encoders with Masked Language Modeling?
    "https://arxiv.org/abs/2507.01006",  # GLM-4.5V and GLM-4.1V-Thinking: Towards Versatile Multimodal Reasoning with Scalable Reinforcement Learning
    "https://arxiv.org/abs/2507.01099",  # Geometry-aware 4D Video Generation for Robot Manipulation
    "https://arxiv.org/abs/2507.01352",  # Skywork-Reward-V2: Scaling Preference Data Curation via Human-AI Synergy
    "https://arxiv.org/abs/2507.01467",  # Representation Entanglement for Generation: Training Diffusion Transformers Is Much Easier Than You Think
    "https://arxiv.org/abs/2507.01544",  # MARVIS: Modality Adaptive Reasoning over VISualizations
    "https://arxiv.org/abs/2507.01643",  # SAILViT: Towards Robust and Generalizable Visual Backbones for MLLMs via Gradual Feature Refinement
    "https://arxiv.org/abs/2507.01679",  # Blending Supervised and Reinforcement Fine-Tuning with Prefix Sampling
    "https://arxiv.org/abs/2507.01701",  # Exploring Advanced LLM Multi-Agent Systems Based on Blackboard Architecture
    "https://arxiv.org/abs/2507.01949",  # Kwai Keye-VL Technical Report
    "https://arxiv.org/abs/2507.01955",  # How Well Does GPT-4o Understand Vision? Evaluating Multimodal Foundation Models on Standard Computer Vision Tasks
    "https://arxiv.org/abs/2507.01961",  # AC-DiT: Adaptive Coordination Diffusion Transformer for Mobile Manipulation
    "https://arxiv.org/abs/2507.02029",  # RoboBrain 2.0 Technical Report
    "https://arxiv.org/abs/2507.02092",  # Energy-Based Transformers are Scalable Learners and Thinkers
    "https://arxiv.org/abs/2507.02199",  # Latent Chain-of-Thought? Decoding the Depth-Recurrent Transformer
    "https://arxiv.org/abs/2507.02861",  # LiteReality: Graphics-Ready 3D Scene Reconstruction from RGB-D Scans
    "https://arxiv.org/abs/2507.02978",  # Ascending the Infinite Ladder: Benchmarking Spatial Deformation Reasoning in Vision-Language Models
    "https://arxiv.org/abs/2507.03112",  # RLVER: Reinforcement Learning with Verifiable Emotion Rewards for Empathetic Agents
    "https://arxiv.org/abs/2507.03285",  # Memory Mosaics at scale
    "https://arxiv.org/abs/2507.03302",  # Leveraging Out-of-Distribution Unlabeled Images: Semi-Supervised Semantic Segmentation with an Open-Vocabulary Model
    "https://arxiv.org/abs/2507.03458",  # Helping CLIP See Both the Forest and the Trees: A Decomposition and Description Approach
    "https://arxiv.org/abs/2507.03657",  # Dynamic Multimodal Prototype Learning in Vision-Language Models
    "https://arxiv.org/abs/2507.04039",  # Generalized Locomotion in Out-of-distribution Conditions with Robust Transformer
    "https://arxiv.org/abs/2507.04103",  # How to Train Your LLM Web Agent: A Statistical Diagnosis
    "https://arxiv.org/abs/2507.04140",  # Learning Humanoid Arm Motion via Centroidal Momentum Regularized Multi-Agent Reinforcement Learning
    "https://arxiv.org/abs/2507.04192",  # JAX-MPM: A Learning-Augmented Differentiable Meshfree Framework for GPU-Accelerated Lagrangian Simulation and Geophysical Inverse Modeling
    "https://arxiv.org/abs/2507.04380",  # Transferring Visual Explainability of Self-Explaining Models through Task Arithmetic
    "https://arxiv.org/abs/2507.04447",  # DreamVLA: A Vision-Language-Action Model Dreamed with Comprehensive World Knowledge
    "https://arxiv.org/abs/2507.04511",  # FA: Forced Prompt Learning of Vision-Language Models for Out-of-Distribution Detection
    "https://arxiv.org/abs/2507.04590",  # VLM2Vec-V2: Advancing Multimodal Embedding for Videos, Images, and Visual Documents
    "https://arxiv.org/abs/2507.05116",  # VOTE: Vision-Language-Action Optimization with Trajectory Ensemble Voting
    "https://arxiv.org/abs/2507.05255",  # Open Vision Reasoner: Transferring Linguistic Cognitive Behavior for Visual Reasoning
    "https://arxiv.org/abs/2507.05258",  # Spatio-Temporal LLM: Reasoning about Environments and Actions
    "https://arxiv.org/abs/2507.05331",  # A Careful Examination of Large Behavior Models for Multitask Dexterous Manipulation
    "https://arxiv.org/abs/2507.05386",  # Reinforcement Fine-Tuning Naturally Mitigates Forgetting in Continual Post-Training
    "https://arxiv.org/abs/2507.05707",  # Agentic-R1: Distilled Dual-Strategy Reasoning
    "https://arxiv.org/abs/2507.05791",  # GTA1: GUI Test-time Scaling Agent
    "https://arxiv.org/abs/2507.05920",  # High-Resolution Visual Reasoning via Multi-Turn Grounding-Based Reinforcement Learning
    "https://arxiv.org/abs/2507.06187",  # The Delta Learning Hypothesis: Preference Tuning on Weak Data can Yield Strong Gains
    "https://arxiv.org/abs/2507.06203",  # A Survey on Latent Reasoning
    "https://arxiv.org/abs/2507.06261",  # Gemini 2.5: Pushing the Frontier with Advanced Reasoning, Multimodality, Long Context, and Next Generation Agentic Capabilities
    "https://arxiv.org/abs/2507.06448",  # Perception-Aware Policy Optimization for Multimodal Reasoning
    "https://arxiv.org/abs/2507.06607",  # Decoder-Hybrid-Decoder Architecture for Efficient Reasoning with Long Generation
    "https://arxiv.org/abs/2507.06710",  # Spatial-Temporal Aware Visuomotor Diffusion Policy Learning
    "https://arxiv.org/abs/2507.06830",  # Physics-Grounded Motion Forecasting via Equation Discovery for Trajectory-Guided Image-to-Video Generation
    "https://arxiv.org/abs/2507.06892",  # Squeeze the Soaked Sponge: Efficient Off-policy Reinforcement Finetuning for Large Language Model
    "https://arxiv.org/abs/2507.06905",  # ULC: A Unified and Fine-Grained Controller for Humanoid Loco-Manipulation
    "https://arxiv.org/abs/2507.07101",  # Small Batch Size Training for Language Models: When Vanilla SGD Works, and Why Gradient Accumulation Is Wasteful
    "https://arxiv.org/abs/2507.07348",  # Zero-Shot Context Generalization in Reinforcement Learning from Few Training Contexts
    "https://arxiv.org/abs/2507.07375",  # Bradley-Terry and Multi-Objective Reward Modeling Are Complementary
    "https://arxiv.org/abs/2507.07610",  # SpatialViz-Bench: A Cognitively-Grounded Benchmark for Diagnosing Spatial Visualization in MLLMs
    "https://arxiv.org/abs/2507.07712",  # Class-wise Balancing Data Replay for Federated Class-Incremental Learning
    "https://arxiv.org/abs/2507.07781",  # SURPRISE3D: A Dataset for Spatial Understanding and Reasoning in Complex 3D Scenes
    "https://arxiv.org/abs/2507.07825",  # Beyond Robustness: Learning Unknown Dynamic Load Adaptation for Quadruped Locomotion on Rough Terrain
    "https://arxiv.org/abs/2507.07969",  # Reinforcement Learning with Action Chunking
    "https://arxiv.org/abs/2507.07986",  # EXPO: Stable Reinforcement Learning with Expressive Policies
    "https://arxiv.org/abs/2507.07995",  # Single-pass Adaptive Image Tokenization for Minimum Program Search
    "https://arxiv.org/abs/2507.07998",  # PyVision: Agentic Vision with Dynamic Tooling
    "https://arxiv.org/abs/2507.07999",  # Traceable Evidence Enhanced Visual Grounded Reasoning: Evaluation and Methodology
    "https://arxiv.org/abs/2507.08068",  # Quantile Reward Policy Optimization: Alignment with Pointwise Regression and Exact Partition Functions
    "https://arxiv.org/abs/2507.08306",  # M2-Reasoning: Empowering MLLMs with Unified General and Spatial Reasoning
    "https://arxiv.org/abs/2507.08656",  # Multi-critic Learning for Whole-body End-effector Twist Tracking
    "https://arxiv.org/abs/2507.08664",  # Introspection of Thought Helps AI Agents
    "https://arxiv.org/abs/2507.08838",  # wd1: Weighted Policy Optimization for Reasoning in Diffusion Language Models
    "https://arxiv.org/abs/2507.08979",  # PRISM: Reducing Spurious Implicit Biases in Vision-Language Models with LLM-Guided Embedding Projection
    "https://arxiv.org/abs/2507.09160",  # Tactile-VLA: Unlocking Vision-Language-Action Model's Physical Knowledge for Tactile Generalization
    "https://arxiv.org/abs/2507.09177",  # Continual Reinforcement Learning by Planning with Online World Models
    "https://arxiv.org/abs/2507.09615",  # Towards Fine-Grained Adaptation of CLIP via a Self-Trained Alignment Score
    "https://arxiv.org/abs/2507.09662",  # Towards Concise and Adaptive Thinking in Large Reasoning Models: A Survey
    "https://arxiv.org/abs/2507.09876",  # ViTCoT: Video-Text Interleaved Chain-of-Thought for Boosting Video Understanding in Large Language Models
    "https://arxiv.org/abs/2507.09961",  # Text-Driven Causal Representation Learning for Source-Free Domain Generalization
    "https://arxiv.org/abs/2507.10069",  # ElasticMM: Efficient Multimodal LLMs Serving with Elastic Multimodal Parallelism
    "https://arxiv.org/abs/2507.10087",  # Foundation Model Driven Robotics: A Comprehensive Review
    "https://arxiv.org/abs/2507.10202",  # A Training-Free, Task-Agnostic Framework for Enhancing MLLM Performance on High-Resolution Images
    "https://arxiv.org/abs/2507.10203",  # Improving Multimodal Learning via Imbalanced Learning
    "https://arxiv.org/abs/2507.10302",  # DisCo: Towards Distinct and Coherent Visual Encapsulation in Video MLLMs
    "https://arxiv.org/abs/2507.10434",  # CLA: Latent Alignment for Online Continual Self-Supervised Learning
    "https://arxiv.org/abs/2507.10442",  # Response Wide Shut? Surprising Observations in Basic Vision Language Model Capabilities
    "https://arxiv.org/abs/2507.10524",  # Mixture-of-Recursions: Learning Dynamic Recursive Depths for Adaptive Token-Level Computation
    "https://arxiv.org/abs/2507.10532",  # Reasoning or Memorization? Unreliable Results of Reinforcement Learning Due to Data Contamination
    "https://arxiv.org/abs/2507.10548",  # EmbRACE-3K: Embodied Reasoning and Action in Complex Environments
    "https://arxiv.org/abs/2507.10672",  # Vision Language Action Models in Robotic Manipulation: A Systematic Review
    "https://arxiv.org/abs/2507.10914",  # Fast Non-Episodic Adaptive Tuning of Robot Controllers with Online Policy Optimization
    "https://arxiv.org/abs/2507.11060",  # Personalized Exercise Recommendation with Semantically-Grounded Knowledge Tracing
    "https://arxiv.org/abs/2507.11269",  # Turning Sand to Gold: Recycling Data to Bridge On-Policy and Off-Policy Learning via Causal Bound
    "https://arxiv.org/abs/2507.11296",  # Diffusion-Based Imaginative Coordination for Bimanual Manipulation
    "https://arxiv.org/abs/2507.11851",  # Your LLM Knows the Future: Uncovering Its Multi-Token Prediction Potential
    "https://arxiv.org/abs/2507.11932",  # Hyperphantasia: A Benchmark for Evaluating the Mental Visualization Capabilities of Multimodal LLMs
    "https://arxiv.org/abs/2507.11948",  # Kevin: Multi-Turn RL for Generating CUDA Kernels
    "https://arxiv.org/abs/2507.11988",  # Aime: Towards Fully-Autonomous Multi-Agent Framework
    "https://arxiv.org/abs/2507.12006",  # Frequency-Dynamic Attention Modulation for Dense Prediction
    "https://arxiv.org/abs/2507.12440",  # EgoVLA: Learning Vision-Language-Action Models from Egocentric Human Videos
    "https://arxiv.org/abs/2507.12465",  # PhysX-3D: Physical-Grounded 3D Asset Generation
    "https://arxiv.org/abs/2507.12507",  # Scaling Up RL: Unlocking Diverse Reasoning in LLMs via Prolonged Training
    "https://arxiv.org/abs/2507.12508",  # MindJourney: Test-Time Scaling with World Models for Spatial Reasoning
    "https://arxiv.org/abs/2507.12846",  # Enter the Mind Palace: Reasoning and Planning for Long-term Active Embodied Question Answering
    "https://arxiv.org/abs/2507.12898",  # Vidar: Embodied Video Diffusion Model for Generalist Manipulation
    "https://arxiv.org/abs/2507.13019",  # Rethinking the Embodied Gap in Vision-and-Language Navigation: A Holistic Study of Physical and Visual Disparities
    "https://arxiv.org/abs/2507.13152",  # SE-VLN: A Self-Evolving Vision-Language Navigation Framework Based on Multimodal Large Language Models
    "https://arxiv.org/abs/2507.13181",  # Spectral Bellman Method: Unifying Representation and Exploration in RL
    "https://arxiv.org/abs/2507.13266",  # QuestA: Expanding Reasoning Capacity in LLMs via Question Augmentation
    "https://arxiv.org/abs/2507.13334",  # A Survey of Context Engineering for Large Language Models
    "https://arxiv.org/abs/2507.13340",  # Latent Policy Steering with Embodiment-Agnostic Pretrained World Models
    "https://arxiv.org/abs/2507.13347",  # $π^3$: Permutation-Equivariant Visual Geometry Learning
    "https://arxiv.org/abs/2507.13348",  # VisionThink: Smart and Efficient Vision Language Model via Reinforcement Learning
    "https://arxiv.org/abs/2507.13362",  # Enhancing Spatial Reasoning in Vision-Language Models via Chain-of-Thought Prompting and Reinforcement Learning
    "https://arxiv.org/abs/2507.13428",  # "PhyWorldBench": A Comprehensive Evaluation of Physical Realism in Text-to-Video Models
    "https://arxiv.org/abs/2507.13579",  # Learning to summarize user information for personalized reinforcement learning from human feedback
    "https://arxiv.org/abs/2507.14049",  # EdgeVLA: Efficient Vision-Language-Action Models
    "https://arxiv.org/abs/2507.14111",  # CUDA-L1: Improving CUDA Optimization via Contrastive Reinforcement Learning
    "https://arxiv.org/abs/2507.14137",  # Franca: Nested Matryoshka Clustering for Scalable Visual Representation Learning
    "https://arxiv.org/abs/2507.14172",  # Self-Improving Language Models for Evolutionary Program Synthesis: A Case Study on ARC-AGI
    "https://arxiv.org/abs/2507.14748",  # Skill Learning via Policy Diversity Yields Identifiable Representations for Reinforcement Learning
    "https://arxiv.org/abs/2507.14793",  # Flow Equivariant Recurrent Neural Networks
    "https://arxiv.org/abs/2507.14901",  # Learning Nonlinear Causal Reductions to Explain Reinforcement Learning Policies
    "https://arxiv.org/abs/2507.14987",  # AlphaAlign: Incentivizing Safety Alignment with Extremely Simplified Reinforcement Learning
    "https://arxiv.org/abs/2507.15216",  # Improving Joint Embedding Predictive Architecture with Diffusion Noise
    "https://arxiv.org/abs/2507.15597",  # Being-H0: Vision-Language-Action Pretraining from Large-Scale Human Videos
    "https://arxiv.org/abs/2507.15824",  # Can Your Model Separate Yolks with a Water Bottle? Benchmarking Physical Commonsense Understanding in Video Generation Models
    "https://arxiv.org/abs/2507.15857",  # Diffusion Beats Autoregressive in Data-Constrained Settings
    "https://arxiv.org/abs/2507.16003",  # Learning without training: The implicit dynamics of in-context learning
    "https://arxiv.org/abs/2507.16406",  # Sparse-View 3D Reconstruction: Recent Advances and Open Challenges
    "https://arxiv.org/abs/2507.16518",  # C2-Evo: Co-Evolving Multimodal Data and Model for Self-Improving Reasoning
    "https://arxiv.org/abs/2507.16577",  # Scaling Linear Attention with Sparse State Expansion
    "https://arxiv.org/abs/2507.16663",  # Turning Internal Gap into Self-Improvement: Promoting the Generation-Understanding Unification in MLLMs
    "https://arxiv.org/abs/2507.16746",  # Zebra-CoT: A Dataset for Interleaved Vision Language Reasoning
    "https://arxiv.org/abs/2507.16806",  # Beyond Binary Rewards: Training LMs to Reason About Their Uncertainty
    "https://arxiv.org/abs/2507.16814",  # Semi-off-Policy Reinforcement Learning for Vision-Language Slow-Thinking Reasoning
    "https://arxiv.org/abs/2507.16815",  # ThinkAct: Vision-Language-Action Reasoning via Reinforced Visual Latent Planning
    "https://arxiv.org/abs/2507.17049",  # Evaluating Uncertainty and Quality of Visual Language Action-enabled Robots
    "https://arxiv.org/abs/2507.17383",  # Confidence Calibration in Vision-Language-Action Models
    "https://arxiv.org/abs/2507.17520",  # InstructVLA: Vision-Language-Action Instruction Tuning from Understanding to Manipulation
    "https://arxiv.org/abs/2507.17634",  # WSM: Decay-Free Learning Rate Schedule via Checkpoint Merging for LLM Pre-training
    "https://arxiv.org/abs/2507.17744",  # Yume: An Interactive World Generation Model
    "https://arxiv.org/abs/2507.17746",  # Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains
    "https://arxiv.org/abs/2507.17842",  # Shop-R1: Rewarding LLMs to Simulate Human Behavior in Online Shopping via Reinforcement Learning
    "https://arxiv.org/abs/2507.18009",  # GRR-CoCa: Leveraging LLM Mechanisms in Multimodal Model Architectures
    "https://arxiv.org/abs/2507.18059",  # Multi-Agent Guided Policy Optimization
    "https://arxiv.org/abs/2507.18071",  # Group Sequence Policy Optimization
    "https://arxiv.org/abs/2507.18074",  # AlphaGo Moment for Model Architecture Discovery
    "https://arxiv.org/abs/2507.18342",  # EgoExoBench: A Benchmark for First- and Third-person View Video Understanding in MLLMs
    "https://arxiv.org/abs/2507.18391",  # Revisiting LLM Reasoning via Information Bottleneck
    "https://arxiv.org/abs/2507.18624",  # Checklists Are Better Than Reward Models For Aligning Language Models
    "https://arxiv.org/abs/2507.19060",  # PurpCode: Reasoning for Safer Code Generation
    "https://arxiv.org/abs/2507.19234",  # Virne: A Comprehensive Benchmark for RL-based Network Resource Allocation in NFV
    "https://arxiv.org/abs/2507.19457",  # GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning
    "https://arxiv.org/abs/2507.19468",  # Back to the Features: DINO as a Foundation for Video World Models
    "https://arxiv.org/abs/2507.19849",  # Agentic Reinforced Policy Optimization
    "https://arxiv.org/abs/2507.20068",  # PERRY: Policy Evaluation with Confidence Intervals using Auxiliary Data
    "https://arxiv.org/abs/2507.20174",  # LRR-Bench: Left, Right or Rotate? Vision-Language models Still Struggle With Spatial Understanding Tasks
    "https://arxiv.org/abs/2507.20187",  # Diversity-Enhanced Reasoning for Subjective Questions
    "https://arxiv.org/abs/2507.20529",  # Enhancing Spatial Reasoning through Visual and Textual Thinking
    "https://arxiv.org/abs/2507.20534",  # Kimi K2: Open Agentic Intelligence
    "https://arxiv.org/abs/2507.20673",  # Geometric-Mean Policy Optimization
    "https://arxiv.org/abs/2507.20766",  # Learning Only with Images: Visual Reinforcement Learning with Reasoning, Rendering, and Visual Feedback
    "https://arxiv.org/abs/2507.20879",  # DriveAgent-R1: Advancing VLM-based Autonomous Driving with Active Perception and Hybrid Thinking
    "https://arxiv.org/abs/2507.21045",  # Reconstructing 4D Spatial Intelligence: A Survey
    "https://arxiv.org/abs/2507.21046",  # A Survey of Self-Evolving Agents: What, When, How, and Where to Evolve on the Path to Artificial Super Intelligence
    "https://arxiv.org/abs/2507.21053",  # Flow Matching Policy Gradients
    "https://arxiv.org/abs/2507.21533",  # Model Predictive Adversarial Imitation Learning for Planning from Observation
    "https://arxiv.org/abs/2507.21848",  # EDGE-GRPO: Entropy-Driven GRPO with Guided Error Correction for Advantage Diversity
    "https://arxiv.org/abs/2507.22003",  # See Different, Think Better: Visual Variations Mitigating Hallucinations in LVLMs
    "https://arxiv.org/abs/2507.22028",  # From Seeing to Experiencing: Scaling Navigation Foundation Models with Reinforcement Learning
    "https://arxiv.org/abs/2507.22062",  # Meta CLIP 2: A Worldwide Scaling Recipe
    "https://arxiv.org/abs/2507.22448",  # Falcon-H1: A Family of Hybrid-Head Language Models Redefining Efficiency and Performance
    "https://arxiv.org/abs/2507.22607",  # VL-Cogito: Progressive Curriculum Reinforcement Learning for Advanced Multimodal Reasoning
    "https://arxiv.org/abs/2507.22844",  # RLVMR: Reinforcement Learning with Verifiable Meta-Reasoning Rewards for Robust Long-Horizon Agents
    "https://arxiv.org/abs/2507.23070",  # Vocabulary-free Fine-grained Visual Recognition via Enriched Contextually Grounded Vision-Language Model
    "https://arxiv.org/abs/2507.23276",  # How Far Are AI Scientists from Changing the World?
    "https://arxiv.org/abs/2507.23278",  # UniLiP: Adapting CLIP for Unified Multimodal Understanding, Generation and Editing
    "https://arxiv.org/abs/2507.23523",  # H-RDT: Human Manipulation Enhanced Bimanual Robotic Manipulation
    "https://arxiv.org/abs/2507.23682",  # villa-X: Enhancing Latent Action Modeling in Vision-Language-Action Models
    "https://arxiv.org/abs/2507.23751",  # CoT-Self-Instruct: Building high-quality synthetic prompts for reasoning and non-reasoning tasks
    "https://arxiv.org/abs/2507.23773",  # SimuRA: A World-Model-Driven Simulative Reasoning Architecture for General Goal-Oriented Agents
    "https://arxiv.org/abs/2508.00410",  # Co-rewarding: Stable Self-supervised RL for Eliciting Reasoning in Large Language Models
    "https://arxiv.org/abs/2508.00795",  # Video Generators are Robot Policies
    "https://arxiv.org/abs/2508.01112",  # MASIV: Toward Material-Agnostic System Identification from Videos
    "https://arxiv.org/abs/2508.01119",  # The Promise of RL for Autoregressive Image Editing
    "https://arxiv.org/abs/2508.01415",  # RoboMemory: A Brain-inspired Multi-memory Agentic Framework for Interactive Environmental Learning in Physical Embodied Systems
    "https://arxiv.org/abs/2508.01558",  # EvoVLMA: Evolutionary Vision-Language Model Adaptation
    "https://arxiv.org/abs/2508.01561",  # One Subgoal at a Time: Zero-Shot Generalization to Arbitrary Linear Temporal Logic Requirements in Multi-Task Reinforcement Learning
    "https://arxiv.org/abs/2508.01695",  # DexReMoE:In-hand Reorientation of General Object via Mixtures of Experts
    "https://arxiv.org/abs/2508.01781",  # A comprehensive taxonomy of hallucinations in Large Language Models
    "https://arxiv.org/abs/2508.02027",  # An Evolving Scenario Generation Method based on Dual-modal Driver Model Trained by Multi-Agent Reinforcement Learning
    "https://arxiv.org/abs/2508.02085",  # SE-Agent: Self-Evolution Trajectory Optimization in Multi-Step Reasoning with LLM-Based Agents
    "https://arxiv.org/abs/2508.02095",  # VLM4D: Towards Spatiotemporal Awareness in Vision Language Models
    "https://arxiv.org/abs/2508.02120",  # Don't Overthink It: A Survey of Efficient R1-style Large Reasoning Models
    "https://arxiv.org/abs/2508.02124",  # Trainable Dynamic Mask Sparse Attention
    "https://arxiv.org/abs/2508.02150",  # Beyond the Trade-off: Self-Supervised Reinforcement Learning for Reasoning Models' Instruction Following
    "https://arxiv.org/abs/2508.02298",  # CAPO: Towards Enhancing LLM Reasoning through Generative Credit Assignment
    "https://arxiv.org/abs/2508.02419",  # Modality Bias in LVLMs: Analyzing and Mitigating Object Hallucination via Attention Lens
    "https://arxiv.org/abs/2508.02549",  # MonoDream: Monocular Vision-Language Navigation with Panoramic Dreaming
    "https://arxiv.org/abs/2508.02671",  # Raw Data Matters: Enhancing Prompt Tuning by Internal Augmentation on Vision-Language Models
    "https://arxiv.org/abs/2508.02948",  # Sample-Efficient Distributionally Robust Multi-Agent Reinforcement Learning via Online Interaction
    "https://arxiv.org/abs/2508.03100",  # AVATAR: Reinforcement Learning to See, Hear, and Reason Over Video
    "https://arxiv.org/abs/2508.03102",  # Causal Disentanglement and Cross-Modal Alignment for Enhanced Few-Shot Learning
    "https://arxiv.org/abs/2508.03339",  # UniFucGrasp: Human-Hand-Inspired Unified Functional Grasp Annotation Strategy and Dataset for Diverse Dexterous Hands
    "https://arxiv.org/abs/2508.03346",  # Making Slow Thinking Faster: Compressing LLM Chain-of-Thought via Step Entropy
    "https://arxiv.org/abs/2508.03613",  # Goedel-Prover-V2: Scaling Formal Theorem Proving with Scaffolded Data Synthesis and Self-Correction
    "https://arxiv.org/abs/2508.03645",  # DiWA: Diffusion Policy Adaptation with World Models
    "https://arxiv.org/abs/2508.03680",  # Agent Lightning: Train ANY AI Agents with Reinforcement Learning
    "https://arxiv.org/abs/2508.03682",  # Self-Questioning Language Models
    "https://arxiv.org/abs/2508.03923",  # CoAct-1: Computer-using Agents with Coding as Actions
    "https://arxiv.org/abs/2508.03944",  # Constraint-Preserving Data Generation for Visuomotor Policy Learning
    "https://arxiv.org/abs/2508.04227",  # Continual Learning for VLMs: A Survey and Taxonomy Beyond Forgetting
    "https://arxiv.org/abs/2508.04324",  # TempFlow-GRPO: When Timing Matters for GRPO in Flow Models
    "https://arxiv.org/abs/2508.04389",  # GuirlVG: Incentivize GUI Visual Grounding via Empirical Exploration on Reinforcement Learning
    "https://arxiv.org/abs/2508.04416",  # Thinking With Videos: Multimodal Tool-Augmented Reinforcement Learning for Long Video Reasoning
    "https://arxiv.org/abs/2508.04700",  # SEAgent: Self-Evolving Computer Use Agent with Autonomous Learning from Experience
    "https://arxiv.org/abs/2508.04816",  # CoMAD: A Multiple-Teacher Self-Supervised Distillation Framework
    "https://arxiv.org/abs/2508.04865",  # Agnostics: Learning to Code in Any Programming Language via Reinforcement with a Universal Learning Environment
    "https://arxiv.org/abs/2508.04942",  # Accelerating Conditional Prompt Learning via Masked Image Modeling for Vision-Language Models
    "https://arxiv.org/abs/2508.04987",  # Unified modality separation: A vision-language framework for unsupervised domain adaptation
    "https://arxiv.org/abs/2508.05004",  # R-Zero: Self-Evolving Reasoning LLM from Zero Data
    "https://arxiv.org/abs/2508.05186",  # Learning to See and Act: Task-Aware Virtual View Exploration for Robotic Manipulation
    "https://arxiv.org/abs/2508.05433",  # Multimodal LLM-assisted Evolutionary Search for Programmatic Control Policies
    "https://arxiv.org/abs/2508.05461",  # How and Why: Taming Flow Matching for Unsupervised Anomaly Detection and Localization
    "https://arxiv.org/abs/2508.05547",  # Adapting Vision-Language Models Without Labels: A Comprehensive Survey
    "https://arxiv.org/abs/2508.05612",  # Shuffle-R1: Efficient RL framework for Multimodal Large Language Models via Data-centric Dynamic Shuffle
    "https://arxiv.org/abs/2508.05629",  # On the Generalization of SFT: A Reinforcement Learning Perspective with Reward Rectification
    "https://arxiv.org/abs/2508.05634",  # Towards Generalizable Safety in Crowd Navigation via Conformal Uncertainty Handling
    "https://arxiv.org/abs/2508.05748",  # WebWatcher: Breaking New Frontier of Vision-Language Deep Research Agent
    "https://arxiv.org/abs/2508.06259",  # SIFThinker: Spatially-Aware Image Focus for Visual Reasoning
    "https://arxiv.org/abs/2508.06317",  # Uncertainty-quantified Rollout Policy Adaptation for Unlabelled Cross-domain Temporal Grounding
    "https://arxiv.org/abs/2508.07033",  # $\mathcal{P}^3$: Toward Versatile Embodied Agents
    "https://arxiv.org/abs/2508.07388",  # Invert4TVG: A Temporal Video Grounding Framework with Inversion Tasks Preserving Action Understanding Ability
    "https://arxiv.org/abs/2508.07407",  # A Comprehensive Survey of Self-Evolving AI Agents: A New Paradigm Bridging Foundation Models and Lifelong Agentic Systems
    "https://arxiv.org/abs/2508.07452",  # Stackelberg Coupling of Online Representation Learning and Reinforcement Learning
    "https://arxiv.org/abs/2508.07804",  # Pose-RFT: Enhancing MLLMs for 3D Pose Generation via Hybrid Action Reinforcement Fine-Tuning
    "https://arxiv.org/abs/2508.07917",  # MolmoAct: Action Reasoning Models that can Reason in Space
    "https://arxiv.org/abs/2508.07976",  # Beyond Ten Turns: Unlocking Long-Horizon Agentic Search with Large-Scale Asynchronous RL
    "https://arxiv.org/abs/2508.08189",  # Reinforcement Learning for Large Model: A Survey
    "https://arxiv.org/abs/2508.08221",  # Part I: Tricks or Traps? A Deep Dive into RL for LLM Reasoning
    "https://arxiv.org/abs/2508.08328",  # Whole-Body Coordination for Dynamic Object Grasping with Legged Manipulators
    "https://arxiv.org/abs/2508.09071",  # GeoVLA: Empowering 3D Representations in Vision-Language-Action Models
    "https://arxiv.org/abs/2508.09726",  # Sample More to Think Less: Group Filtered Policy Optimization for Concise Reasoning
    "https://arxiv.org/abs/2508.09736",  # Seeing, Listening, Remembering, and Reasoning: A Multimodal Agent with Long-Term Memory
    "https://arxiv.org/abs/2508.09834",  # Speed Always Wins: A Survey on Efficient Architectures for Large Language Models
    "https://arxiv.org/abs/2508.10104",  # DINOv3
    "https://arxiv.org/abs/2508.10333",  # ReconVLA: Reconstructive Vision-Language-Action Model as Effective Robot Perceiver
    "https://arxiv.org/abs/2508.10433",  # We-Math 2.0: A Versatile MathBook System for Incentivizing Visual Mathematical Reasoning
    "https://arxiv.org/abs/2508.10538",  # MLM: Learning Multi-task Loco-Manipulation Whole-Body Control for Quadruped Robot with Arm
    "https://arxiv.org/abs/2508.10858",  # Hierarchical Fine-grained Preference Optimization for Physically Plausible Video Generation
    "https://arxiv.org/abs/2508.10874",  # SSRL: Self-Search Reinforcement Learning
    "https://arxiv.org/abs/2508.11117",  # Robot Policy Evaluation for Sim-to-Real Transfer: A Benchmarking Perspective
    "https://arxiv.org/abs/2508.11143",  # Actor-Critic for Continuous Action Chunks: A Reinforcement Learning Framework for Long-Horizon Robotic Manipulation with Sparse Reward
    "https://arxiv.org/abs/2508.11408",  # On-Policy RL Meets Off-Policy Experts: Harmonizing Supervised Fine-Tuning and Reinforcement Learning via Dynamic Weighting
    "https://arxiv.org/abs/2508.11616",  # Controlling Multimodal LLMs via Reward-guided Decoding
    "https://arxiv.org/abs/2508.11630",  # Thyme: Think Beyond Images
    "https://arxiv.org/abs/2508.11737",  # Ovis2.5 Technical Report
    "https://arxiv.org/abs/2508.12109",  # Simple o3: Towards Interleaved Vision-Language Reasoning
    "https://arxiv.org/abs/2508.12137",  # Infusing fine-grained visual knowledge to Vision-Language Models
    "https://arxiv.org/abs/2508.12211",  # Improving Pre-Trained Vision-Language-Action Policies with Model-Based Search
    "https://arxiv.org/abs/2508.12252",  # Robot Trains Robot: Automatic Real-World Policy Adaptation and Learning for Humanoids
    "https://arxiv.org/abs/2508.12466",  # Inverse-LLaVA: Eliminating Alignment Pre-training Through Text-to-Vision Mapping
    "https://arxiv.org/abs/2508.12587",  # Multimodal Chain of Continuous Thought for Latent-Space Reasoning in Vision-Language Models
    "https://arxiv.org/abs/2508.12790",  # Reinforcement Learning with Rubric Anchors
    "https://arxiv.org/abs/2508.13073",  # Large VLM-based Vision-Language-Action Models for Robotic Manipulation: A Survey
    "https://arxiv.org/abs/2508.13142",  # Holistic Evaluation of Multimodal LLMs on Spatial Intelligence
    "https://arxiv.org/abs/2508.13167",  # Chain-of-Agents: End-to-End Agent Foundation Models via Multi-Agent Distillation and Agentic RL
    "https://arxiv.org/abs/2508.13587",  # Breaking the SFT Plateau: Multimodal Structured Reinforcement Learning for Chart-to-Code Generation
    "https://arxiv.org/abs/2508.13755",  # Depth-Breadth Synergy in RLVR: Unlocking LLM Reasoning Gains with Adaptive Exploration
    "https://arxiv.org/abs/2508.13904",  # One-Step Flow Q-Learning: Addressing the Diffusion Policy Bottleneck in Offline Reinforcement Learning
    "https://arxiv.org/abs/2508.13911",  # PhysGM: Large Physical Gaussian Model for Feed-Forward 4D Synthesis
    "https://arxiv.org/abs/2508.14029",  # Beyond Pass@1: Self-Play with Variational Problem Synthesis Sustains RLVR
    "https://arxiv.org/abs/2508.14040",  # ComputerRL: Scaling End-to-End Online Reinforcement Learning for Computer Use Agents
    "https://arxiv.org/abs/2508.14313",  # Your Reward Function for RL is Your Best PRM for Search: Unifying RL and Search-Based TTS
    "https://arxiv.org/abs/2508.14460",  # DuPO: Enabling Reliable LLM Self-Verification via Dual Preference Optimization
    "https://arxiv.org/abs/2508.14881",  # Compute-Optimal Scaling for Value-Based Deep RL
    "https://arxiv.org/abs/2508.15260",  # Deep Think with Confidence
    "https://arxiv.org/abs/2508.15568",  # Backpropagation-Free Test-Time Adaptation via Probabilistic Gaussian Alignment
    "https://arxiv.org/abs/2508.16027",  # Optimal Dynamic Regret by Transformers for Non-Stationary Reinforcement Learning
    "https://arxiv.org/abs/2508.16204",  # Competition and Attraction Improve Model Fusion
    "https://arxiv.org/abs/2508.16546",  # RL Is Neither a Panacea Nor a Mirage: Understanding Supervised vs. Reinforcement Learning Fine-Tuning for LLMs
    "https://arxiv.org/abs/2508.16943",  # LHM-Humanoid: Learning a Unified Policy for Long-Horizon Humanoid Whole-Body Loco-Manipulation in Diverse Messy Environments
    "https://arxiv.org/abs/2508.17298",  # Explain Before You Answer: A Survey on Compositional Visual Reasoning
    "https://arxiv.org/abs/2508.17437",  # Pixie: Fast and Generalizable Supervised Learning of 3D Physics from Pixels
    "https://arxiv.org/abs/2508.17445",  # TreePO: Bridging the Gap of Policy Optimization and Efficacy and Inference Efficiency with Heuristic Tree-based Modeling
    "https://arxiv.org/abs/2508.17600",  # GWM: Towards Scalable Gaussian World Models for Robotic Manipulation
    "https://arxiv.org/abs/2508.17692",  # LLM-based Agentic Reasoning Frameworks: A Survey from Methods to Scenarios
    "https://arxiv.org/abs/2508.17696",  # Fair Cooperation in Mixed-Motive Games via Conflict-Aware Gradient Adjustment
    "https://arxiv.org/abs/2508.17784",  # Proximal Supervised Fine-Tuning
    "https://arxiv.org/abs/2508.17850",  # GEPO: Group Expectation Policy Optimization for Stable Heterogeneous Reinforcement Learning
    "https://arxiv.org/abs/2508.17971",  # Neural Algorithmic Reasoners informed Large Language Model for Multi-Agent Path Finding
    "https://arxiv.org/abs/2508.18269",  # FlowVLA: Visual Chain of Thought-based Motion Reasoning for Vision-Language-Action Models
    "https://arxiv.org/abs/2508.18588",  # History Rhymes: Accelerating LLM Reinforcement Learning with RhymeRL
    "https://arxiv.org/abs/2508.18672",  # Optimal Sparsity of Mixture-of-Experts Language Models for Reasoning Tasks
    "https://arxiv.org/abs/2508.18966",  # USO: Unified Style and Subject-Driven Generation via Disentangled and Reward Learning
    "https://arxiv.org/abs/2508.19005",  # Building Self-Evolving Agents via Experience-Driven Lifelong Learning: A Framework and Benchmark
    "https://arxiv.org/abs/2508.19229",  # StepWiser: Stepwise Generative Judges for Wiser Reasoning
    "https://arxiv.org/abs/2508.19236",  # MemoryVLA: Perceptual-Cognitive Memory in Vision-Language-Action Models for Robotic Manipulation
    "https://arxiv.org/abs/2508.19652",  # Self-Rewarding Vision-Language Model via Reasoning Decomposition
    "https://arxiv.org/abs/2508.19900",  # Adaptive Scaling of Policy Constraints for Offline Reinforcement Learning
    "https://arxiv.org/abs/2508.20072",  # Discrete Diffusion VLA: Bringing Discrete Diffusion to Action Decoding in Vision-Language-Action Policies
    "https://arxiv.org/abs/2508.20294",  # Dynamics-Aligned Latent Imagination in Contextual World Models for Zero-Shot Generalization
    "https://arxiv.org/abs/2508.20722",  # rStar2-Agent: Agentic Reasoning Technical Report
    "https://arxiv.org/abs/2508.20840",  # Learning Primitive Embodied World Models: Towards Scalable Robotic Learning
    "https://arxiv.org/abs/2508.21046",  # CogVLA: Cognition-Aligned Vision-Language-Action Model via Instruction-Driven Routing & Sparsification
    "https://arxiv.org/abs/2508.21065",  # Learning on the Fly: Rapid Policy Adaptation via Differentiable Simulation
    "https://arxiv.org/abs/2508.21107",  # Learning to Generate Unit Test via Adversarial Reinforcement Learning
    "https://arxiv.org/abs/2508.21112",  # EO-1: An Open Unified Embodied Foundation Model for General Robot Control
    "https://arxiv.org/abs/2508.21188",  # Mirage or Method? How Model-Task Alignment Induces Divergent RL Conclusions
    "https://arxiv.org/abs/2509.00361",  # Generative Visual Foresight Meets Task-Agnostic Pose Estimation in Robotic Table-Top Manipulation
    "https://arxiv.org/abs/2509.00421",  # Memory Limitations of Prompt Tuning in Transformers
    "https://arxiv.org/abs/2509.00576",  # Galaxea Open-World Dataset and G0 Dual-System VLA Model
    "https://arxiv.org/abs/2509.00789",  # CogDriver: Integrating Cognitive Inertia for Temporally Coherent Planning in Autonomous Driving
    "https://arxiv.org/abs/2509.01044",  # Hierarchical Reactive Grasping via Task-Space Velocity Fields and Joint-Space Quadratic Programming
    "https://arxiv.org/abs/2509.01055",  # VerlTool: Towards Holistic Agentic Reinforcement Learning with Tool Use
    "https://arxiv.org/abs/2509.01092",  # REFRAG: Rethinking RAG based Decoding
    "https://arxiv.org/abs/2509.01106",  # Robix: A Unified Model for Robot Interaction, Reasoning and Planning
    "https://arxiv.org/abs/2509.01321",  # Towards High Data Efficiency in Reinforcement Learning with Verifiable Reward
    "https://arxiv.org/abs/2509.01644",  # OpenVision 2: A Family of Generative Pretrained Visual Encoders for Multimodal Learning
    "https://arxiv.org/abs/2509.01656",  # Reinforced Visual Perception with Tools
    "https://arxiv.org/abs/2509.01684",  # Reinforcement Learning for Machine Learning Engineering Agents
    "https://arxiv.org/abs/2509.01720",  # Succeed or Learn Slowly: Sample Efficient Off-Policy Reinforcement Learning for Mobile App Control
    "https://arxiv.org/abs/2509.01819",  # ManiFlow: A General Robot Manipulation Policy via Consistency Flow Training
    "https://arxiv.org/abs/2509.01920",  # Dynamic Speculative Agent Planning
    "https://arxiv.org/abs/2509.01944",  # AutoDrive-R$^2$: Incentivizing Reasoning and Self-Reflection Capacity for VLA Model in Autonomous Driving
    "https://arxiv.org/abs/2509.02055",  # Align-Then-stEer: Adapting the Vision-Language Action Models through Unified Latent Guidance
    "https://arxiv.org/abs/2509.02333",  # DCPO: Dynamic Clipping Policy Optimization
    "https://arxiv.org/abs/2509.02350",  # Implicit Reasoning in Large Language Models: A Comprehensive Survey
    "https://arxiv.org/abs/2509.02479",  # SimpleTIR: End-to-End Reinforcement Learning for Multi-Turn Tool-Integrated Reasoning
    "https://arxiv.org/abs/2509.02534",  # Jointly Reinforcing Diversity and Quality in Language Model Generations
    "https://arxiv.org/abs/2509.02547",  # The Landscape of Agentic Reinforcement Learning for LLMs: A Survey
    "https://arxiv.org/abs/2509.02722",  # Planning with Reasoning using Vision Language World Model
    "https://arxiv.org/abs/2509.02815",  # Multi-Embodiment Locomotion at Scale with extreme Embodiment Randomization
    "https://arxiv.org/abs/2509.03113",  # Mitigating Multimodal Hallucinations via Gradient-based Self-Reflection
    "https://arxiv.org/abs/2509.03312",  # AgenTracer: Who Is Inducing Failure in the LLM Agentic Systems?
    "https://arxiv.org/abs/2509.03518",  # Can LLMs Lie? Investigation beyond Hallucination
    "https://arxiv.org/abs/2509.03646",  # Emergent Hierarchical Reasoning in LLMs through Reinforcement Learning
    "https://arxiv.org/abs/2509.03771",  # Co-Evolving Complexity: An Adversarial Framework for Automatic MARL Curricula
    "https://arxiv.org/abs/2509.04018",  # FPC-VLA: A Vision-Language-Action Framework with a Supervisor for Failure Prediction and Correction
    "https://arxiv.org/abs/2509.04063",  # Balancing Signal and Variance: Adaptive Offline RL Post-Training for VLA Flow Models
    "https://arxiv.org/abs/2509.04259",  # RL's Razor: Why Online Reinforcement Learning Forgets Less
    "https://arxiv.org/abs/2509.04501",  # Understanding Reinforcement Learning for Model Training, and future directions with GRAPE
    "https://arxiv.org/abs/2509.04784",  # Post-training Large Language Models for Diverse High-Quality Responses
    "https://arxiv.org/abs/2509.04996",  # FLOWER: Democratizing Generalist Robot Policies with Efficient Vision-Language-Action Flow Policies
    "https://arxiv.org/abs/2509.05193",  # Shift Before You Learn: Enabling Low-Rank Representations in Reinforcement Learning
    "https://arxiv.org/abs/2509.05314",  # ManipDreamer3D : Synthesizing Plausible Robotic Manipulation Video with Occupancy-aware 3D Trajectory
    "https://arxiv.org/abs/2509.05489",  # Self-Aligned Reward: Towards Effective and Efficient Reasoners
    "https://arxiv.org/abs/2509.06040",  # BranchGRPO: Stable and Efficient GRPO with Structured Branching in Diffusion Models
    "https://arxiv.org/abs/2509.06160",  # Reverse-Engineered Reasoning for Open-Ended Generation
    "https://arxiv.org/abs/2509.06342",  # Towards bridging the gap: Systematic sim-to-real transfer for diverse legged robots
    "https://arxiv.org/abs/2509.06782",  # Physics-informed Value Learner for Offline Goal-Conditioned Reinforcement Learning
    "https://arxiv.org/abs/2509.06806",  # MachineLearningLM: Scaling Many-shot In-context Learning via Continued Pretraining
    "https://arxiv.org/abs/2509.06863",  # floq: Training Critics via Flow-Matching for Scaling Compute in Value-Based RL
    "https://arxiv.org/abs/2509.06870",  # The Majority is not always right: RL training for solution aggregation
    "https://arxiv.org/abs/2509.06949",  # Revolutionizing Reinforcement Learning Framework for Diffusion Large Language Models
    "https://arxiv.org/abs/2509.06951",  # F1: A Vision-Language-Action Model Bridging Understanding and Generation to Actions
    "https://arxiv.org/abs/2509.07414",  # Language Self-Play For Data-Free Training
    "https://arxiv.org/abs/2509.07430",  # The Choice of Divergence: A Neglected Key to Mitigating Diversity Collapse in Reinforcement Learning with Verifiable Reward
    "https://arxiv.org/abs/2509.07445",  # Text2Touch: Tactile In-Hand Manipulation with LLM-Designed Reward Functions
    "https://arxiv.org/abs/2509.07945",  # One Model for All Tasks: Leveraging Efficient World Models in Multi-Task Planning
    "https://arxiv.org/abs/2509.07962",  # TA-VLA: Elucidating the Design Space of Torque-aware Vision-Language-Action Models
    "https://arxiv.org/abs/2509.07969",  # Mini-o3: Scaling Up Reasoning Patterns and Interaction Turns for Visual Search
    "https://arxiv.org/abs/2509.07979",  # Visual Representation Alignment for Multimodal Large Language Models
    "https://arxiv.org/abs/2509.07980",  # Parallel-R1: Towards Parallel Thinking via Reinforcement Learning
    "https://arxiv.org/abs/2509.08660",  # Replicable Reinforcement Learning with Linear Function Approximation
    "https://arxiv.org/abs/2509.08755",  # AgentGym-RL: Training LLM Agents for Long-Horizon Decision Making through Multi-Turn Reinforcement Learning
    "https://arxiv.org/abs/2509.08827",  # A Survey of Reinforcement Learning for Large Reasoning Models
    "https://arxiv.org/abs/2509.09090",  # SQAP-VLA: A Synergistic Quantization-Aware Pruning Framework for High-Performance Vision-Language-Action Models
    "https://arxiv.org/abs/2509.09135",  # Continuous-Time Value Iteration for Multi-Agent Reinforcement Learning
    "https://arxiv.org/abs/2509.09284",  # Tree-OPO: Off-policy Monte Carlo Tree-Guided Advantage Optimization for Multistep Reasoning
    "https://arxiv.org/abs/2509.09372",  # VLA-Adapter: An Effective Paradigm for Tiny-Scale Vision-Language-Action Model
    "https://arxiv.org/abs/2509.09666",  # Unified Multimodal Models as Auto-Encoders
    "https://arxiv.org/abs/2509.09674",  # SimpleVLA-RL: Scaling VLA Training via Reinforcement Learning
    "https://arxiv.org/abs/2509.09675",  # CDE: Curiosity-Driven Exploration for Efficient Reinforcement Learning in Large Language Models
    "https://arxiv.org/abs/2509.10396",  # Inpainting-Guided Policy Optimization for Diffusion Large Language Models
    "https://arxiv.org/abs/2509.11197",  # DreamNav: A Trajectory-Based Imaginative Framework for Zero-Shot Vision-and-Language Navigation
    "https://arxiv.org/abs/2509.11348",  # On Linear Mode Connectivity of Mixture-of-Experts Architectures
    "https://arxiv.org/abs/2509.11417",  # Enhancing Generalization in Vision-Language-Action Models by Preserving Pretrained Representations
    "https://arxiv.org/abs/2509.11452",  # Learning to Optimize Multi-Objective Alignment Through Dynamic Reward Weighting
    "https://arxiv.org/abs/2509.11480",  # Cross-Platform Scaling of Vision-Language-Action Models from Edge to Cloud GPUs
    "https://arxiv.org/abs/2509.12026",  # Imitation Learning as Return Distribution Matching
    "https://arxiv.org/abs/2509.12132",  # Look Again, Think Slowly: Enhancing Visual Reflection in Vision-Language Models
    "https://arxiv.org/abs/2509.12249",  # Why and How Auxiliary Tasks Improve JEPA Representations
    "https://arxiv.org/abs/2509.13095",  # Empowering Multi-Robot Cooperation via Sequential World Models
    "https://arxiv.org/abs/2509.13305",  # WebSailor-V2: Bridging the Chasm to Proprietary Agents via Synthetic Data and Scalable Reinforcement Learning
    "https://arxiv.org/abs/2509.13351",  # Teaching LLMs to Plan: Logical Chain-of-Thought Instruction Tuning for Symbolic Planning
    "https://arxiv.org/abs/2509.14117",  # GeoAware-VLA: Implicit Geometry Aware Vision-Language-Action Model
    "https://arxiv.org/abs/2509.14234",  # Compute as Teacher: Turning Inference Compute Into Reference-Free Supervision
    "https://arxiv.org/abs/2509.14252",  # LLM-JEPA: Large Language Models Meet Joint Embedding Predictive Architectures
    "https://arxiv.org/abs/2509.14295",  # Aegis: Automated Error Generation and Attribution for Multi-Agent Systems
    "https://arxiv.org/abs/2509.14760",  # Reasoning over Boundaries: Enhancing Specification Alignment via Test-time Deliberation
    "https://arxiv.org/abs/2509.14889",  # CollabVLA: Self-Reflective Vision-Language-Action Model Dreaming Together with Human
    "https://arxiv.org/abs/2509.15031",  # AutoEdit: Automatic Hyperparameter Tuning for Image Editing
    "https://arxiv.org/abs/2509.15155",  # Self-Improving Embodied Foundation Models
    "https://arxiv.org/abs/2509.15172",  # Internalizing Self-Consistency in Language Models: Multi-Agent Consensus Alignment
    "https://arxiv.org/abs/2509.15194",  # Evolving Language Models without Labels: Majority Drives Selection, Novelty Promotes Variation
    "https://arxiv.org/abs/2509.15207",  # FlowRL: Matching Reward Distributions for LLM Reasoning
    "https://arxiv.org/abs/2509.15273",  # Embodied Arena: A Comprehensive, Unified, and Evolving Evaluation Platform for Embodied AI
    "https://arxiv.org/abs/2509.15443",  # Implicit Kinodynamic Motion Retargeting for Human-to-humanoid Imitation Learning
    "https://arxiv.org/abs/2509.15536",  # SAMPO:Scale-wise Autoregression with Motion PrOmpt for generative world models
    "https://arxiv.org/abs/2509.15607",  # PRIMT: Preference-based Reinforcement Learning with Multimodal Feedback and Trajectory Synthesis from Foundation Models
    "https://arxiv.org/abs/2509.15733",  # GP3: A 3D Geometry-Aware Policy with Multi-View Images for Robotic Manipulation
    "https://arxiv.org/abs/2509.15927",  # Enhancing Generative Auto-bidding with Offline Reward Evaluation and Policy Search
    "https://arxiv.org/abs/2509.15929",  # Improving Monte Carlo Tree Search for Symbolic Regression
    "https://arxiv.org/abs/2509.15937",  # A Vision-Language-Action-Critic Model for Robotic Real-World Reinforcement Learning
    "https://arxiv.org/abs/2509.15965",  # RLinf: Flexible and Efficient Large-scale Reinforcement Learning via Macro-to-Micro Flow Transformation
    "https://arxiv.org/abs/2509.15981",  # Uncertainty-Based Smooth Policy Regularisation for Reinforcement Learning with Few Demonstrations
    "https://arxiv.org/abs/2509.15999",  # Inverse Optimization Latent Variable Models for Learning Costs Applied to Route Problems
    "https://arxiv.org/abs/2509.16072",  # I-FailSense: Towards General Robotic Failure Detection with Vision-Language Models
    "https://arxiv.org/abs/2509.16084",  # Exploring Synthesizable Chemical Space with Iterative Pathway Refinements
    "https://arxiv.org/abs/2509.16117",  # DiffusionNFT: Online Diffusion Reinforcement with Forward Process
    "https://arxiv.org/abs/2509.16127",  # BaseReward: A Strong Baseline for Multimodal Reward Model
    "https://arxiv.org/abs/2509.16500",  # RLGF: Reinforcement Learning with Geometric Feedback for Autonomous Driving Video Generation
    "https://arxiv.org/abs/2509.16606",  # Bayesian Ego-graph Inference for Networked Multi-Agent Reinforcement Learning
    "https://arxiv.org/abs/2509.16865",  # Large Language Models as End-to-end Combinatorial Optimization Solvers
    "https://arxiv.org/abs/2509.16950",  # Temporal Logic-Based Multi-Vehicle Backdoor Attacks against Offline RL Agents in End-to-end Autonomous Driving
    "https://arxiv.org/abs/2509.16965",  # Preference Distillation via Value based Reinforcement Learning
    "https://arxiv.org/abs/2509.17057",  # RoboManipBaselines: A Unified Framework for Imitation Learning in Robotic Manipulation across Real and Simulation Environments
    "https://arxiv.org/abs/2509.17325",  # Generalizable End-to-End Tool-Use RL with Synthetic CodeGym
    "https://arxiv.org/abs/2509.17647",  # VideoArtGS: Building Digital Twins of Articulated Objects from Monocular Video
    "https://arxiv.org/abs/2509.18119",  # MobileRL: Online Agentic Reinforcement Learning for Mobile GUI Agents
    "https://arxiv.org/abs/2509.18376",  # GnnXemplar: Exemplars to Explanations -- Natural Language Rules for Global GNN Interpretability
    "https://arxiv.org/abs/2509.18389",  # Towards Provable Emergence of In-Context Reinforcement Learning
    "https://arxiv.org/abs/2509.18631",  # Generalizable Domain Adaptation for Sim-and-Real Policy Co-Training
    "https://arxiv.org/abs/2509.18644",  # Do You Need Proprioceptive States in Visuomotor Policies?
    "https://arxiv.org/abs/2509.18648",  # SPiDR: A Simple Approach for Zero-Shot Safety in Sim-to-Real Transfer
    "https://arxiv.org/abs/2509.18714",  # A Generalized Bisimulation Metric of State Similarity between Markov Decision Processes: From Theoretical Propositions to Applications
    "https://arxiv.org/abs/2509.18830",  # DexSkin: High-Coverage Conformable Robotic Skin for Learning Contact-Rich Manipulation
    "https://arxiv.org/abs/2509.18891",  # Attack for Defense: Adversarial Agents for Point Prompt Optimization Empowering Segment Anything Model
    "https://arxiv.org/abs/2509.18953",  # Eva-VLA: Evaluating Vision-Language-Action Models' Robustness Under Real-World Physical Variations
    "https://arxiv.org/abs/2509.19003",  # Unveiling Chain of Step Reasoning for Vision-Language Models with Fine-grained Rewards
    "https://arxiv.org/abs/2509.19012",  # Pure Vision Language Action (VLA) Models: A Comprehensive Survey
    "https://arxiv.org/abs/2509.19080",  # World4RL: Diffusion World Models for Policy Refinement with Reinforcement Learning for Robotic Manipulation
    "https://arxiv.org/abs/2509.19170",  # Soft Tokens, Hard Truths
    "https://arxiv.org/abs/2509.19199",  # Agentic Reinforcement Learning with Implicit Step Rewards
    "https://arxiv.org/abs/2509.19292",  # SOE: Sample-Efficient Robot Policy Self-Improvement via On-Manifold Exploration
    "https://arxiv.org/abs/2509.19301",  # Residual Off-Policy RL for Finetuning Behavior Cloning Policies
    "https://arxiv.org/abs/2509.19349",  # ShinkaEvolve: Towards Open-Ended And Sample-Efficient Program Evolution
    "https://arxiv.org/abs/2509.19454",  # ROPA: Synthetic Robot Pose Generation for RGB-D Bimanual Data Augmentation
    "https://arxiv.org/abs/2509.19524",  # Score the Steps, Not Just the Goal: VLM-Based Subgoal Evaluation for Robotic Manipulation
    "https://arxiv.org/abs/2509.19555",  # AnySafe: Adapting Latent Safety Filters at Runtime via Safety Constraint Parameterization in the Latent Space
    "https://arxiv.org/abs/2509.19696",  # Diffusion-Based Impedance Learning for Contact-Rich Manipulation Tasks
    "https://arxiv.org/abs/2509.19800",  # Analysis of approximate linear programming solution to Markov decision problem with log barrier function
    "https://arxiv.org/abs/2509.19846",  # BoreaRL: A Multi-Objective Reinforcement Learning Environment for Climate-Adaptive Boreal Forest Management
    "https://arxiv.org/abs/2509.20021",  # Embodied AI: From LLMs to World Models
    "https://arxiv.org/abs/2509.20109",  # Discrete Diffusion for Reflective Vision-Language-Action Models in Autonomous Driving
    "https://arxiv.org/abs/2509.20234",  # ImageNet-trained CNNs are not biased towards texture: Revisiting feature reliance through controlled suppression
    "https://arxiv.org/abs/2509.20297",  # mindmap: Spatial Memory in Deep Feature Maps for 3D Action Policies
    "https://arxiv.org/abs/2509.20322",  # VisualMimic: Visual Humanoid Loco-Manipulation via Motion Tracking and Generation
    "https://arxiv.org/abs/2509.20357",  # Language Models that Think, Chat Better
    "https://arxiv.org/abs/2509.20358",  # PhysCtrl: Generative Physics for Controllable and Physics-Grounded Video Generation
    "https://arxiv.org/abs/2509.20570",  # PIRF: Physics-Informed Reward Fine-Tuning for Diffusion Models
    "https://arxiv.org/abs/2509.20648",  # Wonder Wins Ways: Curiosity-Driven Exploration through Multi-Agent Contextual Calibration
    "https://arxiv.org/abs/2509.20739",  # Decision-Driven Semantic Object Exploration for Legged Robots via Confidence-Calibrated Perception and Topological Subgoal Selection
    "https://arxiv.org/abs/2509.21016",  # RL Grokking Recipe: How Does RL Unlock and Transfer New Algorithms in LLMs?
    "https://arxiv.org/abs/2509.21044",  # Reinforcement Learning Fine-Tuning Enhances Activation Intensity and Diversity in the Internal Circuitry of LLMs
    "https://arxiv.org/abs/2509.21124",  # Expanding Reasoning Potential in Foundation Model by Learning Diverse Chains of Thought Patterns
    "https://arxiv.org/abs/2509.21128",  # RL Squeezes, SFT Expands: A Comparative Study of Reasoning LLMs
    "https://arxiv.org/abs/2509.21231",  # SEEC: Stable End-Effector Control with Model-Enhanced Residual Learning for Humanoid Loco-Manipulation
    "https://arxiv.org/abs/2509.21240",  # Tree Search for LLM Agent Reinforcement Learning
    "https://arxiv.org/abs/2509.21309",  # NewtonGen: Physics-Consistent and Controllable Text-to-Video Generation via Neural Newtonian Dynamics
    "https://arxiv.org/abs/2509.21319",  # RLBFF: Binary Flexible Feedback to bridge between Human Feedback & Verifiable Rewards
    "https://arxiv.org/abs/2509.21420",  # QuadGPT: Native Quadrilateral Mesh Generation with Autoregressive Models
    "https://arxiv.org/abs/2509.21541",  # ControlHair: Physically-based Video Diffusion for Controllable Dynamic Hair Rendering
    "https://arxiv.org/abs/2509.21723",  # VLBiMan: Vision-Language Anchored One-Shot Demonstration Enables Generalizable Bimanual Robotic Manipulation
    "https://arxiv.org/abs/2509.21792",  # FastGRPO: Accelerating Policy Optimization via Concurrency-aware Speculative Decoding and Online Draft Learning
    "https://arxiv.org/abs/2509.21797",  # MoWM: Mixture-of-World-Models for Embodied Planning via Latent-to-Pixel Feature Modulation
    "https://arxiv.org/abs/2509.21798",  # Evaluating and Improving Cultural Awareness of Reward Models for LLM Alignment
    "https://arxiv.org/abs/2509.21826",  # ResT: Reshaping Token-Level Policy Gradients for Tool-Use Large Language Models
    "https://arxiv.org/abs/2509.21871",  # Unlocking the Essence of Beauty: Advanced Aesthetic Reasoning with Relative-Absolute Policy Optimization
    "https://arxiv.org/abs/2509.21880",  # No Prompt Left Behind: Exploiting Zero-Variance Prompts in LLM Reinforcement Learning via Entropy-Guided Advantage Shaping
    "https://arxiv.org/abs/2509.21942",  # Structural Information-based Hierarchical Diffusion for Offline Reinforcement Learning
    "https://arxiv.org/abs/2509.21953",  # MultiCrafter: High-Fidelity Multi-Subject Generation via Disentangled Attention and Identity-Aware Preference Alignment
    "https://arxiv.org/abs/2509.21986",  # Developing Vision-Language-Action Model from Egocentric Videos
    "https://arxiv.org/abs/2509.21991",  # ERGO: Efficient High-Resolution Visual Understanding for Vision-Language Models
    "https://arxiv.org/abs/2509.22093",  # Action-aware Dynamic Pruning for Efficient Vision-Language-Action Manipulation
    "https://arxiv.org/abs/2509.22114",  # SK2Decompile: LLM-based Two-Phase Binary Decompilation from Skeleton to Skin
    "https://arxiv.org/abs/2509.22149",  # DemoGrasp: Universal Dexterous Grasping from a Single Demonstration
    "https://arxiv.org/abs/2509.22195",  # Actions as Language: Fine-Tuning VLMs into VLAs Without Catastrophic Forgetting
    "https://arxiv.org/abs/2509.22391",  # Do LLM Agents Know How to Ground, Recover, and Assess? A Benchmark for Epistemic Competence in Information-Seeking Agents
    "https://arxiv.org/abs/2509.22485",  # Group Critical-token Policy Optimization for Autoregressive Image Generation
    "https://arxiv.org/abs/2509.22558",  # StepORLM: A Self-Evolving Framework With Generative Process Supervision For Operations Research Language Models
    "https://arxiv.org/abs/2509.22562",  # Activation Function Design Sustains Plasticity in Continual Learning
    "https://arxiv.org/abs/2509.22566",  # From Parameters to Behaviors: Unsupervised Compression of the Policy Space
    "https://arxiv.org/abs/2509.22601",  # Learn the Ropes, Then Trust the Wins: Self-imitation with Progressive Exploration for Agentic Reinforcement Learning
    "https://arxiv.org/abs/2509.22611",  # Quantile Advantage Estimation: Stabilizing RLVR for LLM Reasoning
    "https://arxiv.org/abs/2509.22613",  # Benefits and Pitfalls of Reinforcement Learning for Language Model Planning: A Theoretical Perspective
    "https://arxiv.org/abs/2509.22637",  # Variational Reasoning for Language Models
    "https://arxiv.org/abs/2509.22638",  # Language Models Can Learn from Verbal Feedback Without Scalar Rewards
    "https://arxiv.org/abs/2509.22643",  # VLA-Reasoner: Empowering Vision-Language-Action Models with Reasoning via Online Monte Carlo Tree Search
    "https://arxiv.org/abs/2509.22644",  # WebGen-Agent: Enhancing Interactive Website Generation with Multi-Level Feedback and Step-Level Reinforcement Learning
    "https://arxiv.org/abs/2509.22647",  # CapRL: Stimulating Dense Image Caption Capabilities via Reinforcement Learning
    "https://arxiv.org/abs/2509.22652",  # Pixel Motion Diffusion is What We Need for Robot Control
    "https://arxiv.org/abs/2509.22807",  # MTRec: Learning to Align with User Preferences via Mental Reward Models
    "https://arxiv.org/abs/2509.22824",  # Critique-Coder: Enhancing Coder Models by Critique Reinforcement Learning
    "https://arxiv.org/abs/2509.22970",  # Robot Learning from Any Images
    "https://arxiv.org/abs/2509.22989",  # Towards Strategic Persuasion with Language Models
    "https://arxiv.org/abs/2509.23040",  # Look Back to Reason Forward: Revisitable Memory for Long-Context LLM Agents
    "https://arxiv.org/abs/2509.23075",  # In-Hand Manipulation of Articulated Tools with Dexterous Robot Hands with Sim-to-Real Transfer
    "https://arxiv.org/abs/2509.23102",  # Multiplayer Nash Preference Optimization
    "https://arxiv.org/abs/2509.23203",  # CE-Nav: Flow-Guided Reinforcement Refinement for Cross-Embodiment Local Navigation
    "https://arxiv.org/abs/2509.23236",  # Self-Consistency as a Free Lunch: Reducing Hallucinations in Vision-Language Models via Self-Reflection
    "https://arxiv.org/abs/2509.23250",  # Training Vision-Language Process Reward Models for Test-Time Scaling in Multimodal Reasoning: Key Insights and Lessons Learned
    "https://arxiv.org/abs/2509.23285",  # Toward Effective Tool-Integrated Reasoning via Self-Evolved Preference Learning
    "https://arxiv.org/abs/2509.23330",  # Structured In-context Environment Scaling for Large Language Model Reasoning
    "https://arxiv.org/abs/2509.23652",  # ReWatch-R1: Boosting Complex Video Reasoning in Large Vision-Language Models through Agentic Data Synthesis
    "https://arxiv.org/abs/2509.23653",  # Don't Settle Too Early: Self-Reflective Remasking for Diffusion Language Models
    "https://arxiv.org/abs/2509.23657",  # Beyond English-Centric Training: How Reinforcement Learning Improves Cross-Lingual Reasoning in LLMs
    "https://arxiv.org/abs/2509.23745",  # LocoFormer: Generalist Locomotion via Long-context Adaptation
    "https://arxiv.org/abs/2509.23753",  # Anchored Supervised Fine-Tuning
    "https://arxiv.org/abs/2509.23791",  # CaRe-BN: Precise Moving Statistics for Stabilizing Spiking Neural Networks in Reinforcement Learning
    "https://arxiv.org/abs/2509.23802",  # STAIR: Addressing Stage Misalignment through Temporal-Aligned Preference Reinforcement Learning
    "https://arxiv.org/abs/2509.23829",  # DexFlyWheel: A Scalable and Self-improving Data Generation Framework for Dexterous Manipulation
    "https://arxiv.org/abs/2509.23846",  # Adversarial Diffusion for Robust Reinforcement Learning
    "https://arxiv.org/abs/2509.23863",  # SPELL: Self-Play Reinforcement Learning for Evolving Long-Context Language Models
    "https://arxiv.org/abs/2509.23909",  # EditScore: Unlocking Online RL for Image Editing via High-Fidelity Reward Modeling
    "https://arxiv.org/abs/2509.23931",  # AutoPrune: Each Complexity Deserves a Pruning Policy
    "https://arxiv.org/abs/2509.23958",  # Reinforcement Learning with Inverse Rewards for World Model Post-training
    "https://arxiv.org/abs/2509.23962",  # Conditional Advantage Estimation for Reinforcement Learning in Large Reasoning Models
    "https://arxiv.org/abs/2509.24067",  # In-Context Compositional Q-Learning for Offline Reinforcement Learning
    "https://arxiv.org/abs/2509.24107",  # Fathom-DeepResearch: Unlocking Long Horizon Information Retrieval and Synthesis for SLMs
    "https://arxiv.org/abs/2509.24130",  # Beyond Magic Words: Sharpness-Aware Prompt Evolving for Robust Large Language Models with TARE
    "https://arxiv.org/abs/2509.24156",  # Reasoning or Retrieval? A Study of Answer Attribution on Large Reasoning Models
    "https://arxiv.org/abs/2509.24203",  # Group-Relative REINFORCE Is Secretly an Off-Policy Algorithm: Demystifying Some Myths About GRPO and Its Friends
    "https://arxiv.org/abs/2509.24207",  # Humanline: Online Alignment as Perceptual Loss
    "https://arxiv.org/abs/2509.24251",  # Latent Visual Reasoning
    "https://arxiv.org/abs/2509.24261",  # Risk-Sensitive RL for Alleviating Exploration Dilemmas in Large Language Models
    "https://arxiv.org/abs/2509.24304",  # FrameThinker: Learning to Think with Long Videos via Multi-Turn Frame Spotlighting
    "https://arxiv.org/abs/2509.24305",  # Asynchronous Policy Gradient Aggregation for Efficient Distributed Reinforcement Learning
    "https://arxiv.org/abs/2509.24372",  # Evolution Strategies at Scale: LLM Fine-Tuning Beyond Reinforcement Learning
    "https://arxiv.org/abs/2509.24375",  # Reinforcement Mid-Training
    "https://arxiv.org/abs/2509.24527",  # Training Agents Inside of Scalable World Models
    "https://arxiv.org/abs/2509.24661",  # CEDex: Cross-Embodiment Dexterous Grasp Generation at Scale from Human-like Contact Representations
    "https://arxiv.org/abs/2509.24702",  # Enhancing Physical Plausibility in Video Generation by Reasoning the Implausibility
    "https://arxiv.org/abs/2509.24726",  # Socratic-Zero : Bootstrapping Reasoning via Data-Free Agent Co-evolution
    "https://arxiv.org/abs/2509.24748",  # Robust Policy Expansion for Offline-to-Online RL under Diverse Data Corruption
    "https://arxiv.org/abs/2509.24804",  # DyMoDreamer: World Modeling with Dynamic Modulation
    "https://arxiv.org/abs/2509.24869",  # Retro*: Optimizing LLMs for Reasoning-Intensive Document Retrieval
    "https://arxiv.org/abs/2509.24923",  # When Greedy Wins: Emergent Exploitation Bias in Meta-Bandit LLM Training
    "https://arxiv.org/abs/2509.24948",  # RehearseVLA: Simulated Post-Training for VLAs with Physically-Consistent World Model
    "https://arxiv.org/abs/2509.24981",  # Random Policy Valuation is Enough for LLM Reasoning with Verifiable Rewards
    "https://arxiv.org/abs/2509.25040",  # A multiscale analysis of mean-field transformers in the moderate interaction regime
    "https://arxiv.org/abs/2509.25047",  # Scaling Synthetic Task Generation for Agents via Exploration
    "https://arxiv.org/abs/2509.25055",  # AlphaSAGE: Structure-Aware Alpha Mining via GFlowNets for Robust Exploration
    "https://arxiv.org/abs/2509.25133",  # Rethinking Entropy Regularization in Large Reasoning Models
    "https://arxiv.org/abs/2509.25140",  # ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory
    "https://arxiv.org/abs/2509.25174",  # XQC: Well-conditioned Optimization Accelerates Deep Reinforcement Learning
    "https://arxiv.org/abs/2509.25190",  # Visual Jigsaw Post-Training Improves MLLMs
    "https://arxiv.org/abs/2509.25373",  # From Perception to Cognition: A Survey of Vision-Language Interactive Reasoning in Multimodal Large Language Models
    "https://arxiv.org/abs/2509.25411",  # Boolean Satisfiability via Imitation Learning
    "https://arxiv.org/abs/2509.25424",  # Polychromic Objectives for Reinforcement Learning
    "https://arxiv.org/abs/2509.25449",  # Joint Embeddings Go Temporal
    "https://arxiv.org/abs/2509.25454",  # DeepSearch: Overcome the Bottleneck of Reinforcement Learning with Verifiable Rewards via Monte Carlo Tree Search
    "https://arxiv.org/abs/2509.25541",  # Vision-Zero: Scalable VLM Self-Improvement via Strategic Gamified Self-Play
    "https://arxiv.org/abs/2509.25666",  # Nudging the Boundaries of LLM Reasoning
    "https://arxiv.org/abs/2509.25681",  # dVLA: Diffusion Vision-Language-Action Model with Multimodal Chain-of-Thought
    "https://arxiv.org/abs/2509.25727",  # Boundary-to-Region Supervision for Offline Safe Reinforcement Learning
    "https://arxiv.org/abs/2509.25756",  # SAC Flow: Sample-Efficient Reinforcement Learning of Flow-Based Policies via Velocity-Reparameterized Sequential Modeling
    "https://arxiv.org/abs/2509.25762",  # OPPO: Accelerating PPO-based RLHF via Pipeline Overlap
    "https://arxiv.org/abs/2509.25774",  # PCPO: Proportionate Credit Policy Optimization for Aligning Image Generation Models
    "https://arxiv.org/abs/2509.25787",  # Self-Evolving Vision-Language Models for Image Quality Assessment via Voting and Ranking
    "https://arxiv.org/abs/2509.25794",  # Point-It-Out: Benchmarking Embodied Reasoning for Vision Language Models in Multi-Stage Visual Grounding
    "https://arxiv.org/abs/2509.25810",  # Learning to Reason as Action Abstractions with Scalable Mid-Training RL
    "https://arxiv.org/abs/2509.25827",  # Overthinking Reduction with Decoupled Rewards and Curriculum Data Scheduling
    "https://arxiv.org/abs/2509.25848",  # More Thought, Less Accuracy? On the Dual Nature of Reasoning in Vision-Language Models
    "https://arxiv.org/abs/2509.25849",  # Knapsack RL: Unlocking Exploration of LLMs via Optimizing Budget Allocation
    "https://arxiv.org/abs/2509.25852",  # Reinforced Embodied Planning with Verifiable Reward for Real-World Robotic Manipulation
    "https://arxiv.org/abs/2509.26074",  # Limited Preference Data? Learning Better Reward Model with Latent Space Synthesis
    "https://arxiv.org/abs/2509.26209",  # Diversity-Incentivized Exploration for Versatile Reasoning
    "https://arxiv.org/abs/2509.26226",  # Thinking-Free Policy Initialization Makes Distilled Reasoning Models More Effective and Efficient Reasoners
    "https://arxiv.org/abs/2509.26346",  # EditReward: A Human-Aligned Reward Model for Instruction-Guided Image Editing
    "https://arxiv.org/abs/2509.26354",  # Your Agent May Misevolve: Emergent Risks in Self-evolving LLM Agents
    "https://arxiv.org/abs/2509.26364",  # Data-to-Energy Stochastic Dynamics
    "https://arxiv.org/abs/2509.26578",  # Linking Process to Outcome: Conditional Reward Modeling for LLM Reasoning
    "https://arxiv.org/abs/2509.26601",  # MENLO: From Preferences to Proficiency -- Evaluating and Modeling Native-like Quality Across 47 Languages
    "https://arxiv.org/abs/2509.26605",  # Fine-tuning Behavioral Cloning Policies with Preference-Based Reinforcement Learning
    "https://arxiv.org/abs/2509.26625",  # Learning to See Before Seeing: Demystifying LLM Visual Priors from Language Pre-training
    "https://arxiv.org/abs/2509.26626",  # Recursive Self-Aggregation Unlocks Deep Thinking in Large Language Models
    "https://arxiv.org/abs/2509.26628",  # Attention as a Compass: Efficient Exploration for Process-Supervised RL in Reasoning Models
    "https://arxiv.org/abs/2509.26633",  # OmniRetarget: Interaction-Preserving Data Generation for Humanoid Whole-Body Loco-Manipulation and Scene Interaction
    "https://arxiv.org/abs/2510.00034",  # Review of Hallucination Understanding in Large Language and Vision Models
    "https://arxiv.org/abs/2510.00037",  # On Robustness of Vision-Language-Action Model against Multi-Modal Perturbations
    "https://arxiv.org/abs/2510.00219",  # Thoughtbubbles: an Unsupervised Method for Parallel Thinking in Latent Space
    "https://arxiv.org/abs/2510.00406",  # VLA-RFT: Vision-Language-Action Reinforcement Fine-tuning with Verified Rewards in World Simulators
    "https://arxiv.org/abs/2510.00430",  # PromptLoop: Plug-and-Play Prompt Refinement via Latent Feedback for Diffusion Model Alignment
    "https://arxiv.org/abs/2510.00502",  # Diffusion Alignment as Variational Expectation-Maximization
    "https://arxiv.org/abs/2510.00553",  # On Predictability of Reinforcement Learning Dynamics for Large Language Models
    "https://arxiv.org/abs/2510.00600",  # Hybrid Training for Vision-Language-Action Models
    "https://arxiv.org/abs/2510.00695",  # HAMLET: Switch your Vision-Language-Action Model into a History-Aware Policy
    "https://arxiv.org/abs/2510.00739",  # TD-JEPA: Latent-predictive Representations for Zero-Shot Reinforcement Learning
    "https://arxiv.org/abs/2510.00819",  # Stabilizing Policy Gradients for Sample-Efficient Reinforcement Learning in LLM Reasoning
    "https://arxiv.org/abs/2510.00855",  # Can World Models Benefit VLMs for World Dynamics?
    "https://arxiv.org/abs/2510.00861",  # Erase to Improve: Erasable Reinforcement Learning for Search-Augmented LLMs
    "https://arxiv.org/abs/2510.00911",  # RiskPO: Risk-based Policy Optimization via Verifiable Reward for LLM Post-Training
    "https://arxiv.org/abs/2510.00974",  # JEPA-T: Joint-Embedding Predictive Architecture with Text Fusion for Image Generation
    "https://arxiv.org/abs/2510.01010",  # ImageDoctor: Diagnosing Text-to-Image Generation via Grounded Image Reasoning
    "https://arxiv.org/abs/2510.01037",  # CurES: From Gradient Analysis to Efficient Curriculum Learning for Reasoning LLMs
    "https://arxiv.org/abs/2510.01068",  # Compose Your Policies! Improving Diffusion-based or Flow-based Robot Policies via Test-time Distribution-level Composition
    "https://arxiv.org/abs/2510.01088",  # Safety Instincts: LLMs Learn to Trust Their Internal Compass for Self-Defense
    "https://arxiv.org/abs/2510.01132",  # A Practitioner's Guide to Multi-turn Agentic Reinforcement Learning
    "https://arxiv.org/abs/2510.01135",  # Prompt Curriculum Learning for Efficient LLM Post-Training
    "https://arxiv.org/abs/2510.01143",  # Generalized Parallel Scaling with Interdependent Generations
    "https://arxiv.org/abs/2510.01161",  # Prosperity before Collapse: How Far Can Off-Policy RL Reach with Stale Data on LLMs?
    "https://arxiv.org/abs/2510.01183",  # EvoWorld: Evolving Panoramic World Generation with Explicit 3D Memory
    "https://arxiv.org/abs/2510.01264",  # A Framework for Scalable Heterogeneous Multi-Agent Adversarial Reinforcement Learning in IsaacLab
    "https://arxiv.org/abs/2510.01265",  # RLP: Reinforcement as a Pretraining Objective
    "https://arxiv.org/abs/2510.01399",  # Resolving the Identity Crisis in Text-to-Image Generation
    "https://arxiv.org/abs/2510.01456",  # SCOPED: Score-Curvature Out-of-distribution Proximity Evaluator for Diffusion
    "https://arxiv.org/abs/2510.01539",  # Executable Counterfactuals: Improving LLMs' Causal Reasoning Through Code
    "https://arxiv.org/abs/2510.01540",  # Towards Better Optimization For Listwise Preference in Diffusion Models
    "https://arxiv.org/abs/2510.01607",  # ActiveUMI: Robotic Manipulation with Active Perception from Robot-Free Human Demonstrations
    "https://arxiv.org/abs/2510.01623",  # VLA-R1: Enhancing Reasoning in Vision-Language-Action Models
    "https://arxiv.org/abs/2510.01624",  # Quagmires in SFT-RL Post-Training: When High SFT Scores Mislead and What to Use Instead
    "https://arxiv.org/abs/2510.01642",  # FailSafe: Reasoning and Recovery from Failures in Vision-Language-Action Models
    "https://arxiv.org/abs/2510.01656",  # Asymmetric Proximal Policy Optimization: mini-critics boost LLM reasoning
    "https://arxiv.org/abs/2510.01764",  # Octax: Accelerated CHIP-8 Arcade Environments for Reinforcement Learning in JAX
    "https://arxiv.org/abs/2510.01832",  # SCRIBES: Web-Scale Script-Based Semi-Structured Data Extraction with Reinforcement Learning
    "https://arxiv.org/abs/2510.01982",  # Fine-Grained GRPO for Precise Preference Alignment in Flow Models
    "https://arxiv.org/abs/2510.02172",  # RESTRAIN: From Spurious Votes to Signals -- Self-Driven RL with Self-Penalization
    "https://arxiv.org/abs/2510.02173",  # Learning to Reason for Hallucination Span Detection
    "https://arxiv.org/abs/2510.02180",  # GRACE: A Language Model Framework for Explainable Inverse Reinforcement Learning
    "https://arxiv.org/abs/2510.02240",  # RewardMap: Tackling Sparse Rewards in Fine-grained Visual Reasoning via Multi-Stage Reinforcement Learning
    "https://arxiv.org/abs/2510.02245",  # ExGRPO: Learning to Reason from Experience
    "https://arxiv.org/abs/2510.02252",  # Retargeting Matters: General Motion Retargeting for Humanoid Motion Tracking
    "https://arxiv.org/abs/2510.02263",  # RLAD: Training LLMs to Discover Abstractions for Solving Reasoning Problems
    "https://arxiv.org/abs/2510.02268",  # Do You Know Where Your Camera Is? View-Invariant Policy Learning with Camera Conditioning
    "https://arxiv.org/abs/2510.02284",  # Learning to Generate Rigid Body Interactions with Video Diffusion Models
    "https://arxiv.org/abs/2510.02286",  # Tree-based Dialogue Reinforced Policy Optimization for Red-Teaming Attacks
    "https://arxiv.org/abs/2510.02292",  # From Behavioral Performance to Internal Competence: Interpreting Vision-Language Models with VLM-Lens
    "https://arxiv.org/abs/2510.02298",  # ARMADA: Autonomous Online Failure Detection and Human Shared Control Empower Scalable Real-world Deployment and Adaptation
    "https://arxiv.org/abs/2510.02311",  # Inferring Dynamic Physical Properties from Video Foundation Models
    "https://arxiv.org/abs/2510.02386",  # On The Fragility of Benchmark Contamination Detection in Reasoning Models
    "https://arxiv.org/abs/2510.02590",  # Use the Online Network If You Can: Towards Fast and Stable Reinforcement Learning
    "https://arxiv.org/abs/2510.02654",  # Smart-GRPO: Smartly Sampling Noise for Efficient RL of Flow-Matching Models
    "https://arxiv.org/abs/2510.02665",  # Self-Improvement in Multimodal Large Language Models: A Survey
    "https://arxiv.org/abs/2510.02752",  # The Path of Self-Evolving Large Language Models: Achieving Data-Efficient Learning via Intrinsic Feedback
    "https://arxiv.org/abs/2510.02850",  # Reward Model Routing in Alignment
    "https://arxiv.org/abs/2510.02880",  # Consolidating Reinforcement Learning for Multimodal Discrete Diffusion Models
    "https://arxiv.org/abs/2510.03022",  # HumanoidExo: Scalable Whole-Body Humanoid Manipulation via Wearable Exoskeleton
    "https://arxiv.org/abs/2510.03222",  # Low-probability Tokens Sustain Exploration in Reinforcement Learning with Verifiable Reward
    "https://arxiv.org/abs/2510.03257",  # Triple-BERT: Do We Really Need MARL for Order Dispatch on Ride-Sharing Platforms?
    "https://arxiv.org/abs/2510.03259",  # Meta-Awareness Enhances Reasoning Models: Self-Alignment Reinforcement Learning
    "https://arxiv.org/abs/2510.03269",  # General Exploratory Bonus for Optimistic Exploration in RLHF
    "https://arxiv.org/abs/2510.03471",  # A Simulation Evaluation Suite for Robust Adaptive Quadcopter Control
    "https://arxiv.org/abs/2510.03578",  # Latent Mixture of Symmetries for Sample-Efficient Dynamic Learning
    "https://arxiv.org/abs/2510.03669",  # Token Hidden Reward: Steering Exploration-Exploitation in Group Relative Deep Reinforcement Learning
    "https://arxiv.org/abs/2510.03817",  # TROLL: Trust Regions improve Reinforcement Learning for Large Language Models
    "https://arxiv.org/abs/2510.03827",  # LIBERO-PRO: Towards Robust and Fair Evaluation of Vision-Language-Action Models Beyond Memorization
    "https://arxiv.org/abs/2510.03885",  # Seeing the Bigger Picture: 3D Latent Mapping for Mobile Manipulation Policy Learning
    "https://arxiv.org/abs/2510.04072",  # Slow-Fast Policy Optimization: Reposition-Before-Update for LLM Reasoning
    "https://arxiv.org/abs/2510.04080",  # PoLi-RL: A Point-to-List Reinforcement Learning Framework for Conditional Semantic Textual Similarity
    "https://arxiv.org/abs/2510.04140",  # Selective Expert Guidance for Effective and Diverse Exploration in Reinforcement Learning of LLMs
    "https://arxiv.org/abs/2510.04354",  # Reliable and Scalable Robot Policy Evaluation with Imperfect Simulators
    "https://arxiv.org/abs/2510.04474",  # DRPO: Efficient Reasoning via Decoupled Reward Policy Optimization
    "https://arxiv.org/abs/2510.04507",  # Wavelet Predictive Representations for Non-Stationary Reinforcement Learning
    "https://arxiv.org/abs/2510.04618",  # Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models
    "https://arxiv.org/abs/2510.04871",  # Less is More: Recursive Reasoning with Tiny Networks
    "https://arxiv.org/abs/2510.04978",  # Aligning Perception, Reasoning, Modeling and Interaction: A Survey on Physical AI
    "https://arxiv.org/abs/2510.05057",  # StaMo: Unsupervised Learning of Generalizable Robot Motion from Compact State Representation
    "https://arxiv.org/abs/2510.05069",  # SwiReasoning: Switch-Thinking in Latent and Explicit for Pareto-Superior Reasoning LLMs
    "https://arxiv.org/abs/2510.05560",  # HoloScene: Simulation-Ready Interactive 3D Worlds from a Single Video
    "https://arxiv.org/abs/2510.05571",  # Presenting a Paper is an Art: Self-Improvement Aesthetic Agents for Academic Presentations
    "https://arxiv.org/abs/2510.05580",  # MetaVLA: Unified Meta Co-training For Efficient Embodied Adaption
    "https://arxiv.org/abs/2510.05592",  # In-the-Flow Agentic System Optimization for Effective Planning and Tool Use
    "https://arxiv.org/abs/2510.05681",  # Verifier-free Test-Time Sampling for Vision Language Action Models
    "https://arxiv.org/abs/2510.05837",  # EEPO: Exploration-Enhanced Policy Optimization via Sample-Then-Forget
    "https://arxiv.org/abs/2510.06068",  # MachaGrasp: Morphology-Aware Cross-Embodiment Dexterous Hand Articulation Generation for Grasping
    "https://arxiv.org/abs/2510.06077",  # When Thinking Drifts: Evidential Grounding for Robust Video Reasoning
    "https://arxiv.org/abs/2510.06096",  # The Alignment Auditor: A Bayesian Framework for Verifying and Refining LLM Objectives
    "https://arxiv.org/abs/2510.06179",  # Differentiable Model Predictive Control on the GPU
    "https://arxiv.org/abs/2510.06217",  # TaTToo: Tool-Grounded Thinking PRM for Test-Time Scaling in Tabular Reasoning
    "https://arxiv.org/abs/2510.06251",  # Physics Knowledge in Frontier Models: A Diagnostic Study of Failure Modes
    "https://arxiv.org/abs/2510.06499",  # Webscale-RL: Automated Data Pipeline for Scaling RL Data to Pretraining Levels
    "https://arxiv.org/abs/2510.06540",  # Scalable Policy-Based RL Algorithms for POMDPs
    "https://arxiv.org/abs/2510.06557",  # The Markovian Thinker: Architecture-Agnostic Linear Scaling of Reasoning
    "https://arxiv.org/abs/2510.06647",  # Q-Learning with Fine-Grained Gap-Dependent Regret
    "https://arxiv.org/abs/2510.06649",  # Local Reinforcement Learning with Action-Conditioned Root Mean Squared Q-Functions
    "https://arxiv.org/abs/2510.06673",  # Heptapod: Language Modeling on Visual Signals
    "https://arxiv.org/abs/2510.06710",  # RLinf-VLA: A Unified and Efficient Framework for Reinforcement Learning of Vision-Language-Action Models
    "https://arxiv.org/abs/2510.06714",  # Dual Goal Representations
    "https://arxiv.org/abs/2510.06738",  # AWM: Accurate Weight-Matrix Fingerprint for Large Language Models
    "https://arxiv.org/abs/2510.06783",  # TTRV: Test-Time Reinforcement Learning for Vision Language Models
    "https://arxiv.org/abs/2510.06954",  # From Condensation to Rank Collapse: A Two-Stage Analysis of Transformer Training Dynamics
    "https://arxiv.org/abs/2510.07077",  # Vision-Language-Action Models for Robotics: A Review Towards Real-World Applications
    "https://arxiv.org/abs/2510.07094",  # Sampling Strategies for Robust Universal Quadrupedal Locomotion Policies
    "https://arxiv.org/abs/2510.07152",  # DPL: Depth-only Perceptive Humanoid Locomotion via Realistic Depth Synthesis and Cross-Attention Terrain Reconstruction
    "https://arxiv.org/abs/2510.07206",  # EigenScore: OOD Detection using Posterior Covariance in Diffusion Models
    "https://arxiv.org/abs/2510.07242",  # Hybrid Reinforcement: When Reward Is Sparse, It's Better to Be Dense
    "https://arxiv.org/abs/2510.07550",  # TRAVL: A Recipe for Making Video-Language Models Better Judges of Physics Implausibility
    "https://arxiv.org/abs/2510.07650",  # Value Flows
    "https://arxiv.org/abs/2510.07730",  # DEAS: DEtached value learning with Action Sequence for Scalable Offline RL
    "https://arxiv.org/abs/2510.07794",  # HiPRAG: Hierarchical Process Rewards for Efficient Agentic Retrieval Augmented Generation
    "https://arxiv.org/abs/2510.07915",  # MARC: Memory-Augmented RL Token Compression for Efficient Video Understanding
    "https://arxiv.org/abs/2510.07958",  # A$^2$Search: Ambiguity-Aware Question Answering with Reinforcement Learning
    "https://arxiv.org/abs/2510.08022",  # FastUMI-100K: Advancing Data-driven Robotic Manipulation with a Large-scale UMI-style Dataset
    "https://arxiv.org/abs/2510.08131",  # Real-Time Motion-Controllable Autoregressive Video Diffusion
    "https://arxiv.org/abs/2510.08189",  # R-Horizon: How Far Can Your Large Reasoning Model Really Go in Breadth and Depth?
    "https://arxiv.org/abs/2510.08191",  # Training-Free Group Relative Policy Optimization
    "https://arxiv.org/abs/2510.08240",  # The Alignment Waltz: Jointly Training Agents to Collaborate for Safety
    "https://arxiv.org/abs/2510.08255",  # Opponent Shaping in LLM Agents
    "https://arxiv.org/abs/2510.08398",  # VideoVerse: Does Your T2V Generator Have World Model Capability to Synthesize Videos?
    "https://arxiv.org/abs/2510.08425",  # Reinforcing Diffusion Models by Direct Group Preference Optimization
    "https://arxiv.org/abs/2510.08480",  # Video-STAR: Reinforcing Open-Vocabulary Action Recognition with Tools
    "https://arxiv.org/abs/2510.08529",  # CoMAS: Co-Evolving Multi-Agent Systems via Interaction Rewards
    "https://arxiv.org/abs/2510.08531",  # SpatialLadder: Progressive Training for Spatial Reasoning in Vision-Language Models
    "https://arxiv.org/abs/2510.08540",  # MM-HELIX: Boosting Multimodal Long-Chain Reflective Reasoning with Holistic Platform and Adaptive Hybrid Policy Optimization
    "https://arxiv.org/abs/2510.08549",  # Entropy Regularizing Activation: Boosting Continuous Control, Large Language Models, and Image Classification with Activation as Entropy Constraints
    "https://arxiv.org/abs/2510.08553",  # Dream to Recall: Imagination-Guided Experience Retrieval for Memory-Persistent Vision-and-Language Navigation
    "https://arxiv.org/abs/2510.08554",  # Improving Reasoning for Diffusion Language Models via Group Diffusion Policy Optimization
    "https://arxiv.org/abs/2510.08558",  # Agent Learning via Early Experience
    "https://arxiv.org/abs/2510.08568",  # NovaFlow: Zero-Shot Manipulation via Actionable Flow from Generated Videos
    "https://arxiv.org/abs/2510.08575",  # ReSplat: Learning Recurrent Gaussian Splatting
    "https://arxiv.org/abs/2510.08638",  # Into the Rabbit Hull: From Task-Relevant Concepts in DINO to Minkowski Geometry
    "https://arxiv.org/abs/2510.08673",  # Thinking with Camera: A Unified Multimodal Model for Camera-Centric Understanding and Generation
    "https://arxiv.org/abs/2510.08696",  # Don't Waste Mistakes: Leveraging Negative RL-Groups via Confidence Reweighting
    "https://arxiv.org/abs/2510.08807",  # Humanoid Everyday: A Comprehensive Robotic Dataset for Open-World Humanoid Manipulation
    "https://arxiv.org/abs/2510.08964",  # Unleashing Perception-Time Scaling to Multimodal Reasoning Models
    "https://arxiv.org/abs/2510.08985",  # Rethinking Reasoning in Document Ranking: Why Chain-of-Thought Falls Short
    "https://arxiv.org/abs/2510.09001",  # DARO: Difficulty-Aware Reweighting Policy Optimization
    "https://arxiv.org/abs/2510.09036",  # iMoWM: Taming Interactive Multi-Modal World Model for Robotic Manipulation
    "https://arxiv.org/abs/2510.09201",  # Multimodal Prompt Optimization: Why Not Leverage Multiple Modalities for MLLMs
    "https://arxiv.org/abs/2510.09259",  # Detecting Data Contamination from Reinforcement Learning Post-training for Large Language Models
    "https://arxiv.org/abs/2510.09285",  # Spotlight on Token Perception for Multimodal Reinforcement Learning
    "https://arxiv.org/abs/2510.09312",  # Verifying Chain-of-Thought Reasoning via Its Computational Graph
    "https://arxiv.org/abs/2510.09459",  # Failure Prediction at Runtime for Generative Robot Policies
    "https://arxiv.org/abs/2510.09541",  # SPG: Sandwiched Policy Gradient for Masked Diffusion Language Models
    "https://arxiv.org/abs/2510.09543",  # Guiding Energy-Efficient Locomotion through Impact Mitigation Rewards
    "https://arxiv.org/abs/2510.09577",  # Dyna-Mind: Learning to Simulate from Experience for Better AI Agents
    "https://arxiv.org/abs/2510.09586",  # Vision Language Models: A Survey of 26K Papers
    "https://arxiv.org/abs/2510.09606",  # SpaceVista: All-Scale Visual Spatial Reasoning from mm to km
    "https://arxiv.org/abs/2510.09733",  # VisRAG 2.0: Evidence-Guided Multi-Image Reasoning in Visual Retrieval-Augmented Generation
    "https://arxiv.org/abs/2510.09734",  # ARROW: An Adaptive Rollout and Routing Method for Global Weather Forecasting
    "https://arxiv.org/abs/2510.09817",  # Cross-Sensor Touch Generation
    "https://arxiv.org/abs/2510.09872",  # WARC-Bench: Web Archive Based Benchmark for GUI Subtask Executions
    "https://arxiv.org/abs/2510.09951",  # Emergence of Spatial Representation in an Actor-Critic Agent with Hippocampus-Inspired Sequence Generator
    "https://arxiv.org/abs/2510.09976",  # Reinforcement Fine-Tuning of Flow-Matching Policies for Vision-Language-Action Models
    "https://arxiv.org/abs/2510.10125",  # Ctrl-World: A Controllable Generative World Model for Robot Manipulation
    "https://arxiv.org/abs/2510.10181",  # Dejavu: Towards Experience Feedback Learning for Embodied Intelligence
    "https://arxiv.org/abs/2510.10197",  # Don't Just Fine-tune the Agent, Tune the Environment
    "https://arxiv.org/abs/2510.10274",  # X-VLA: Soft-Prompted Transformer as Scalable Cross-Embodiment Vision-Language-Action Model
    "https://arxiv.org/abs/2510.10487",  # Towards Self-Refinement of Vision-Language Models with Triangular Consistency
    "https://arxiv.org/abs/2510.10509",  # MARS-Sep: Multimodal-Aligned Reinforced Sound Separation
    "https://arxiv.org/abs/2510.10603",  # EA4LLM: A Gradient-Free Approach to Large Language Model Optimization via Evolutionary Algorithms
    "https://arxiv.org/abs/2510.10606",  # ViSurf: Visual Supervised-and-Reinforcement Fine-Tuning for Large Vision-and-Language Models
    "https://arxiv.org/abs/2510.10637",  # High-Fidelity Simulated Data Generation for Real-World Zero-Shot Robotic Manipulation Learning with Gaussian Splatting
    "https://arxiv.org/abs/2510.10644",  # Hierarchical Optimization via LLM-Guided Objective Evolution for Mobility-on-Demand Systems
    "https://arxiv.org/abs/2510.10851",  # Preference-Conditioned Multi-Objective RL for Integrated Command Tracking and Force Compliance in Humanoid Locomotion
    "https://arxiv.org/abs/2510.10903",  # Towards a Unified Understanding of Robot Manipulation: A Comprehensive Survey
    "https://arxiv.org/abs/2510.10937",  # Neutral Agent-based Adversarial Policy Learning against Deep Reinforcement Learning in Multi-party Open Systems
    "https://arxiv.org/abs/2510.11027",  # Vlaser: Vision-Language-Action Model with Synergistic Embodied Reasoning
    "https://arxiv.org/abs/2510.11062",  # Stronger-MAS: Multi-Agent Reinforcement Learning for Collaborative LLMs
    "https://arxiv.org/abs/2510.11103",  # A Primer on SO(3) Action Representations in Deep Reinforcement Learning
    "https://arxiv.org/abs/2510.11106",  # Compositional Zero-Shot Learning: A Survey
    "https://arxiv.org/abs/2510.11121",  # Refining Hybrid Genetic Search for CVRP via Reinforcement Learning-Finetuned LLM
    "https://arxiv.org/abs/2510.11194",  # Aligning Deep Implicit Preferences by Learning to Reason Defensively
    "https://arxiv.org/abs/2510.11258",  # DemoHLM: From One Demonstration to Generalizable Humanoid Loco-Manipulation
    "https://arxiv.org/abs/2510.11369",  # Reasoning as Representation: Rethinking Visual Reinforcement Learning in Image Quality Assessment
    "https://arxiv.org/abs/2510.11495",  # How Reinforcement Learning After Next-Token Prediction Facilitates Learning
    "https://arxiv.org/abs/2510.11512",  # LikePhys: Evaluating Intuitive Physics Understanding in Video Diffusion Models via Likelihood Preference
    "https://arxiv.org/abs/2510.11549",  # ODI-Bench: Can MLLMs Understand Immersive Omnidirectional Environments?
    "https://arxiv.org/abs/2510.11653",  # MATH-Beyond: A Benchmark for RL to Expand Beyond the Base Model
    "https://arxiv.org/abs/2510.11661",  # SR-Scientist: Scientific Equation Discovery With Agentic AI
    "https://arxiv.org/abs/2510.11686",  # Representation-Based Exploration for Language Models: From Test-Time to Post-Training
    "https://arxiv.org/abs/2510.11689",  # Phys2Real: Fusing VLM Priors with Interactive Online Adaptation for Uncertainty-Aware Sim-to-Real Manipulation
    "https://arxiv.org/abs/2510.11696",  # QeRL: Beyond Efficiency -- Quantization-enhanced Reinforcement Learning for LLMs
    "https://arxiv.org/abs/2510.11769",  # GAR: Generative Adversarial Reinforcement Learning for Formal Theorem Proving
    "https://arxiv.org/abs/2510.11824",  # Empirical Study on Robustness and Resilience in Cooperative Multi-Agent Reinforcement Learning
    "https://arxiv.org/abs/2510.12157",  # Self-Verifying Reflection Helps Transformers with CoT Reasoning
    "https://arxiv.org/abs/2510.12225",  # HoneyBee: Data Recipes for Vision-Language Reasoners
    "https://arxiv.org/abs/2510.12264",  # Reducing Belief Deviation in Reinforcement Learning for Active Reasoning
    "https://arxiv.org/abs/2510.12276",  # Spatial Forcing: Implicit Spatial Representation Alignment for Vision-language-action Model
    "https://arxiv.org/abs/2510.12312",  # Deep SPI: Safe Policy Improvement via World Models
    "https://arxiv.org/abs/2510.12603",  # Reasoning in the Dark: Interleaved Vision-Text Reasoning in Latent Space
    "https://arxiv.org/abs/2510.12693",  # ERA: Transforming VLMs into Embodied Agents via Embodied Prior Learning and Online Reinforcement Learning
    "https://arxiv.org/abs/2510.12710",  # Reflection-Based Task Adaptation for Self-Improving VLA
    "https://arxiv.org/abs/2510.12796",  # DriveVLA-W0: World Models Amplify Data Scaling Law in Autonomous Driving
    "https://arxiv.org/abs/2510.12798",  # Detect Anything via Next Point Prediction
    "https://arxiv.org/abs/2510.13054",  # VLA-0: Building State-of-the-Art VLAs with Zero Modification
    "https://arxiv.org/abs/2510.13220",  # EvoTest: Evolutionary Test-Time Learning for Self-Improving Agentic Systems
    "https://arxiv.org/abs/2510.13237",  # Model-agnostic Adversarial Attack and Defense for Vision-Language-Action Models
    "https://arxiv.org/abs/2510.13324",  # Tactile-Conditioned Diffusion Policy for Force-Aware Robotic Manipulation
    "https://arxiv.org/abs/2510.13328",  # Thompson Sampling via Fine-Tuning of LLMs
    "https://arxiv.org/abs/2510.13375",  # DepthVLA: Enhancing Vision-Language-Action Models with Depth-Aware Spatial Reasoning
    "https://arxiv.org/abs/2510.13418",  # Reinforcement Learning Meets Masked Generative Models: Mask-GRPO for Text-to-Image Generation
    "https://arxiv.org/abs/2510.13626",  # LIBERO-Plus: In-depth Robustness Analysis of Vision-Language-Action Models
    "https://arxiv.org/abs/2510.13704",  # Simplicial Embeddings Improve Sample Efficiency in Actor-Critic Agents
    "https://arxiv.org/abs/2510.13778",  # InternVLA-M1: A Spatially Guided Vision-Language-Action Framework for Generalist Robot Policy
    "https://arxiv.org/abs/2510.13786",  # The Art of Scaling Reinforcement Learning Compute for LLMs
    "https://arxiv.org/abs/2510.13800",  # Reasoning in Space via Grounding in the World
    "https://arxiv.org/abs/2510.13809",  # PhysMaster: Mastering Physical Representation for Video Generation via Reinforcement Learning
    "https://arxiv.org/abs/2510.14117",  # ViTacGen: Robotic Pushing with Vision-to-Touch Generation
    "https://arxiv.org/abs/2510.14129",  # Demystifying the Mechanisms Behind Emergent Exploration in Goal-conditioned RL
    "https://arxiv.org/abs/2510.14176",  # ARM-FM: Automated Reward Machines via Foundation Models for Compositional Reinforcement Learning
    "https://arxiv.org/abs/2510.14246",  # Policy Regularized Distributionally Robust Markov Decision Processes with Linear Function Approximation
    "https://arxiv.org/abs/2510.14255",  # Identity-Preserving Image-to-Video Generation via Reward-Guided Optimization
    "https://arxiv.org/abs/2510.14420",  # Instructions are all you need: Self-supervised Reinforcement Learning for Instruction Following
    "https://arxiv.org/abs/2510.14427",  # Deep Compositional Phase Diffusion for Long Motion Sequence Generation
    "https://arxiv.org/abs/2510.14454",  # Towards Adaptable Humanoid Control via Adaptive Motion Tracking
    "https://arxiv.org/abs/2510.14605",  # Knowledge-based Visual Question Answer with Multimodal Processing, Retrieval and Filtering
    "https://arxiv.org/abs/2510.14635",  # ATGen: Adversarial Reinforcement Learning for Test Case Generation
    "https://arxiv.org/abs/2510.14768",  # Leveraging Neural Descriptor Fields for Learning Contact-Aware Dynamic Recovery
    "https://arxiv.org/abs/2510.14836",  # QDepth-VLA: Quantized Depth Prediction as Auxiliary Supervision for Vision-Language-Action Models
    "https://arxiv.org/abs/2510.14901",  # Reasoning with Sampling: Your Base Model is Smarter Than You Think
    "https://arxiv.org/abs/2510.14930",  # VT-Refine: Learning Bimanual Assembly with Visuo-Tactile Feedback via Simulation Fine-Tuning
    "https://arxiv.org/abs/2510.14943",  # LaSeR: Reinforcement Learning with Last-Token Self-Rewarding
    "https://arxiv.org/abs/2510.14959",  # CBF-RL: Safety Filtering Reinforcement Learning in Training with Control Barrier Functions
    "https://arxiv.org/abs/2510.14967",  # Information Gain-based Policy Optimization: A Simple and Effective Approach for Multi-Turn Search Agents
    "https://arxiv.org/abs/2510.14968",  # RDD: Retrieval-Based Demonstration Decomposer for Planner Alignment in Long-Horizon Tasks
    "https://arxiv.org/abs/2510.15040",  # Composition-Grounded Data Synthesis for Visual Reasoning
    "https://arxiv.org/abs/2510.15047",  # Internalizing World Models via Self-Play Finetuning for Agentic RL
    "https://arxiv.org/abs/2510.15242",  # Dual-Weighted Reinforcement Learning for Generative Preference Modeling
    "https://arxiv.org/abs/2510.15352",  # GaussGym: An open-source real-to-sim framework for learning locomotion from pixels
    "https://arxiv.org/abs/2510.15382",  # Towards Robust Zero-Shot Reinforcement Learning
    "https://arxiv.org/abs/2510.15414",  # MARSHAL: Incentivizing Multi-Agent Reasoning via Self-Play with Strategic LLMs
    "https://arxiv.org/abs/2510.15440",  # Select Less, Reason More: Prioritizing Evidence Purity for Video Reasoning
    "https://arxiv.org/abs/2510.15700",  # ProofOptimizer: Training Language Models to Simplify Proofs without Human Demonstrations
    "https://arxiv.org/abs/2510.15839",  # Learning Correlated Reward Models: Statistical Barriers and Opportunities
    "https://arxiv.org/abs/2510.16079",  # EvolveR: Self-Evolving LLM Agents through an Experience-Driven Lifecycle
    "https://arxiv.org/abs/2510.16166",  # Extending Prediction-Powered Inference through Conformal Prediction
    "https://arxiv.org/abs/2510.16281",  # Do What You Say: Steering Vision-Language-Action Models via Runtime Reasoning-Action Alignment Verification
    "https://arxiv.org/abs/2510.16333",  # RL makes MLLMs see better than SFT
    "https://arxiv.org/abs/2510.16416",  # SSL4RL: Revisiting Self-supervised Learning as Intrinsic Reward for Visual-Language Reasoning
    "https://arxiv.org/abs/2510.16596",  # SHIELD: Suppressing Hallucinations In LVLM Encoders via Bias and Vulnerability Defense
    "https://arxiv.org/abs/2510.16614",  # Count Counts: Motivating Exploration in LLM Reasoning with Count-based Intrinsic Rewards
    "https://arxiv.org/abs/2510.16714",  # SceneCOT: Eliciting Grounded Chain-of-Thought Reasoning in 3D Scenes
    "https://arxiv.org/abs/2510.16729",  # Vision-Centric 4D Occupancy Forecasting and Planning via Implicit Residual World Models
    "https://arxiv.org/abs/2510.16732",  # A Comprehensive Survey on World Models for Embodied AI
    "https://arxiv.org/abs/2510.16932",  # Prompt-MII: Meta-Learning Instruction Induction for LLMs
    "https://arxiv.org/abs/2510.17045",  # Video Reasoning without Training
    "https://arxiv.org/abs/2510.17111",  # Efficient Vision-Language-Action Models for Embodied Manipulation: A Systematic Survey
    "https://arxiv.org/abs/2510.17439",  # From Spatial to Actions: Grounding Vision-Language-Action Model in Spatial Foundation Priors
    "https://arxiv.org/abs/2510.17472",  # Certified Self-Consistency: Statistical Guarantees and Test-Time Training for Reliable Reasoning in LLMs
    "https://arxiv.org/abs/2510.17793",  # Foundational Automatic Evaluators: Scaling Multi-Task Generative Evaluator Training for Reasoning-Centric Domains
    "https://arxiv.org/abs/2510.17801",  # Robobench: A Comprehensive Evaluation Benchmark for Multimodal Large Language Models as Embodied Brain
    "https://arxiv.org/abs/2510.17950",  # RoboChallenge: Large-scale Real-robot Evaluation of Embodied Policies
    "https://arxiv.org/abs/2510.18060",  # SPACeR: Self-Play Anchoring with Centralized Reference Models
    "https://arxiv.org/abs/2510.18091",  # Accelerating Vision Transformers with Adaptive Patch Sizes
    "https://arxiv.org/abs/2510.18135",  # World-in-World: World Models in a Closed-Loop World
    "https://arxiv.org/abs/2510.18316",  # MoMaGen: Generating Demonstrations under Soft and Hard Constraints for Multi-Step Bimanual Mobile Manipulation
    "https://arxiv.org/abs/2510.18798",  # WebSeer: Training Deeper Search Agents through Reinforcement Learning with Self-Reflection
    "https://arxiv.org/abs/2510.18821",  # Search Self-play: Pushing the Frontier of Agent Capability without Supervision
    "https://arxiv.org/abs/2510.18873",  # DSI-Bench: A Benchmark for Dynamic Spatial Intelligence
    "https://arxiv.org/abs/2510.18927",  # BAPO: Stabilizing Off-Policy Reinforcement Learning for LLMs via Balanced Policy Optimization with Adaptive Clipping
    "https://arxiv.org/abs/2510.19245",  # See, Think, Act: Online Shopper Behavior Simulation with VLM Agents
    "https://arxiv.org/abs/2510.19307",  # Unified Reinforcement and Imitation Learning for Vision-Language Models
    "https://arxiv.org/abs/2510.19315",  # Transformers are Inherently Succinct
    "https://arxiv.org/abs/2510.19363",  # LoongRL: Reinforcement Learning for Advanced Reasoning over Long Contexts
    "https://arxiv.org/abs/2510.19400",  # Seeing Across Views: Benchmarking Spatial Reasoning of Vision-Language Models in Robotic Scenes
    "https://arxiv.org/abs/2510.19430",  # GigaBrain-0: A World Model-Powered Vision-Language-Action Model
    "https://arxiv.org/abs/2510.19788",  # Benchmarking World-Model Learning with Environment-Level Queries
    "https://arxiv.org/abs/2510.19807",  # Scaf-GRPO: Scaffolded Group Relative Policy Optimization for Enhancing LLM Reasoning
    "https://arxiv.org/abs/2510.19818",  # Semantic World Models
    "https://arxiv.org/abs/2510.20150",  # Rank-GRPO: Training LLM-based Conversational Recommender Systems with Reinforcement Learning
    "https://arxiv.org/abs/2510.20264",  # Optimistic Task Inference for Behavior Foundation Models
    "https://arxiv.org/abs/2510.20286",  # UI-Ins: Enhancing GUI Grounding with Multi-Perspective Instruction-as-Reasoning
    "https://arxiv.org/abs/2510.20328",  # MemER: Scaling Up Memory for Robot Control via Experience Retrieval
    "https://arxiv.org/abs/2510.20413",  # Why DPO is a Misspecified Estimator and How to Fix It
    "https://arxiv.org/abs/2510.20470",  # Conan: Progressive Learning to Reason Like a Detective over Multi-Scale Visual Evidence
    "https://arxiv.org/abs/2510.20607",  # Generalizable Reasoning through Compositional Energy Minimization
    "https://arxiv.org/abs/2510.20685",  # C-NAV: Towards Self-Evolving Continual Object Navigation in Open World
    "https://arxiv.org/abs/2510.20774",  # FieldGen: From Teleoperated Pre-Manipulation Trajectories to Field-Guided Data Generation
    "https://arxiv.org/abs/2510.20813",  # GSWorld: Closed-Loop Photo-Realistic Simulation Suite for Robotic Manipulation
    "https://arxiv.org/abs/2510.20817",  # KL-Regularized Reinforcement Learning is Designed to Mode Collapse
    "https://arxiv.org/abs/2510.20994",  # VESSA: Video-based objEct-centric Self-Supervised Adaptation for Visual Foundation Models
    "https://arxiv.org/abs/2510.21223",  # Model Merging with Functional Dual Anchors
    "https://arxiv.org/abs/2510.21232",  # How Hard is it to Confuse a World Model?
    "https://arxiv.org/abs/2510.21307",  # Towards Physically Executable 3D Gaussian for Embodied Navigation
    "https://arxiv.org/abs/2510.21311",  # FineRS: Fine-grained Reasoning and Segmentation of Small Objects with Reinforcement Learning
    "https://arxiv.org/abs/2510.21447",  # PhysWorld: From Real Videos to World Models of Deformable Objects via Physics-Aware Demonstration Synthesis
    "https://arxiv.org/abs/2510.21501",  # GranViT: A Fine-Grained Vision Model With Autoregressive Perception For MLLMs
    "https://arxiv.org/abs/2510.21571",  # Scalable Vision-Language-Action Model Pretraining for Robotic Manipulation with Real-Life Human Activity Videos
    "https://arxiv.org/abs/2510.21817",  # VITA-E: Natural Embodied Interaction with Concurrent Seeing, Hearing, Speaking, and Acting
    "https://arxiv.org/abs/2510.21840",  # Improving the Physics of Video Generation with VJEPA-2 Reward Signal
    "https://arxiv.org/abs/2510.21890",  # The Principles of Diffusion Models
    "https://arxiv.org/abs/2510.22201",  # ACG: Action Coherence Guidance for Flow-based Vision-Language-Action models
    "https://arxiv.org/abs/2510.22319",  # GRPO-Guard: Mitigating Implicit Over-Optimization in Flow Matching via Regulated Clipping
    "https://arxiv.org/abs/2510.22512",  # Transitive RL: Value Learning via Divide and Conquer
    "https://arxiv.org/abs/2510.22543",  # FAPO: Flawed-Aware Policy Optimization for Efficient and Reliable Reasoning
    "https://arxiv.org/abs/2510.22832",  # HRM-Agent: Training a recurrent reasoning model in dynamic environments using reinforcement learning
    "https://arxiv.org/abs/2510.22975",  # VoMP: Predicting Volumetric Mechanical Property Fields
    "https://arxiv.org/abs/2510.23038",  # Incentivizing Agentic Reasoning in LLM Judges via Tool-Integrated Reinforcement Learning
    "https://arxiv.org/abs/2510.23272",  # Code Aesthetics with Agentic Reward Feedback
    "https://arxiv.org/abs/2510.23473",  # Video-Thinker: Sparking "Thinking with Videos" via Reinforcement Learning
    "https://arxiv.org/abs/2510.23479",  # MergeMix: A Unified Augmentation Paradigm for Visual and Multi-Modal Understanding
    "https://arxiv.org/abs/2510.23486",  # Learning to Reason Efficiently with Discounted Reinforcement Learning
    "https://arxiv.org/abs/2510.23497",  # VOLD: Reasoning Transfer from LLMs to Vision-Language Models via On-Policy Distillation
    "https://arxiv.org/abs/2510.23569",  # EgoThinker: Unveiling Egocentric Reasoning with Spatio-Temporal CoT
    "https://arxiv.org/abs/2510.23571",  # RobotArena $\infty$: Scalable Robot Benchmarking via Real-to-Sim Translation
    "https://arxiv.org/abs/2510.23595",  # Multi-Agent Evolve: LLM Self-Improve through Co-evolution
    "https://arxiv.org/abs/2510.23596",  # Think Twice: Branch-and-Rethink Reasoning Reward Model
    "https://arxiv.org/abs/2510.23603",  # PixelRefer: A Unified Framework for Spatio-Temporal Object Referring with Arbitrary Granularity
    "https://arxiv.org/abs/2510.23763",  # RoboOmni: Proactive Robot Manipulation in Omni-modal Context
    "https://arxiv.org/abs/2510.23925",  # Latent Chain-of-Thought for Visual Reasoning
    "https://arxiv.org/abs/2510.24285",  # ViPER: Empowering the Self-Evolution of Visual Perception Abilities in Vision-Language Model
    "https://arxiv.org/abs/2510.24302",  # Lookahead Tree-Based Rollouts for Enhanced Trajectory-Level Exploration in Reinforcement Learning with Verifiable Rewards
    "https://arxiv.org/abs/2510.24320",  # Critique-RL: Training Language Models for Critiquing through Two-Stage Reinforcement Learning
    "https://arxiv.org/abs/2510.24482",  # Sample-efficient and Scalable Exploration in Continuous-Time RL
    "https://arxiv.org/abs/2510.24673",  # Learning constitutive models and rheology from partial flow measurements
    "https://arxiv.org/abs/2510.24684",  # SPICE: Self-Play In Corpus Environments Improves Reasoning
    "https://arxiv.org/abs/2510.24795",  # A Survey on Efficient Vision-Language-Action Models
    "https://arxiv.org/abs/2510.24832",  # Scheduling Your LLM Reinforcement Learning with Reasoning Trees
    "https://arxiv.org/abs/2510.25405",  # Sim-to-Real Gentle Manipulation of Deformable and Fragile Objects with Stress-Guided Reinforcement Learning
    "https://arxiv.org/abs/2510.25725",  # A Humanoid Visual-Tactile-Action Dataset for Contact-Rich Manipulation
    "https://arxiv.org/abs/2510.25741",  # Scaling Latent Reasoning via Looped Language Models
    "https://arxiv.org/abs/2510.25801",  # Metis-SPECS: Decoupling Multimodal Learning via Self-distilled Preference-based Cold Start
    "https://arxiv.org/abs/2510.25889",  # $π_\texttt{RL}$: Online RL Fine-tuning for Flow-based Vision-Language-Action Models
    "https://arxiv.org/abs/2510.25943",  # InputDSA: Demixing then Comparing Recurrent and Externally Driven Dynamics
    "https://arxiv.org/abs/2510.25992",  # Supervised Reinforcement Learning: From Expert Trajectories to Step-wise Reasoning
    "https://arxiv.org/abs/2510.26280",  # Thor: Towards Human-Level Whole-Body Reactions for Intense Contact-Rich Environments
    "https://arxiv.org/abs/2510.26406",  # Human-in-the-loop Online Rejection Sampling for Robotic Manipulation
    "https://arxiv.org/abs/2510.26433",  # Co-Evolving Latent Action World Models
    "https://arxiv.org/abs/2510.26493",  # Context Engineering 2.0: The Context of Context Engineering
    "https://arxiv.org/abs/2510.26583",  # Emu3.5: Native Multimodal Models are World Learners
    "https://arxiv.org/abs/2510.26742",  # Running VLAs at Real-time Speed
    "https://arxiv.org/abs/2510.26788",  # Defeating the Training-Inference Mismatch via FP16
    "https://arxiv.org/abs/2510.26865",  # Do Vision-Language Models Measure Up? Benchmarking Visual Measurement Reading with MeasureBench
    "https://arxiv.org/abs/2510.27363",  # ToolScope: An Agentic Framework for Vision-Guided and Long-Horizon Tool Use
    "https://arxiv.org/abs/2510.27419",  # DeepCompress: A Dual Reward Strategy for Dynamically Exploring and Compressing Reasoning Chains
    "https://arxiv.org/abs/2510.27492",  # ThinkMorph: Emergent Properties in Multimodal Interleaved Chain-of-Thought Reasoning
    "https://arxiv.org/abs/2510.27566",  # Interact-RAG: Reason and Interact with the Corpus, Beyond Black-Box Retrieval
    "https://arxiv.org/abs/2510.27606",  # Spatial-SSRL: Enhancing Spatial Understanding via Self-Supervised Reinforcement Learning
    "https://arxiv.org/abs/2510.27607",  # Dual-Stream Diffusion for World-Model Augmented Vision-Language-Action Model
    "https://arxiv.org/abs/2511.00062",  # World Simulation with Video Foundation Models for Physical AI
    "https://arxiv.org/abs/2511.00091",  # Self-Improving Vision-Language-Action Models with Data Generation via Residual RL
    "https://arxiv.org/abs/2511.00108",  # Pelican-VL 1.0: A Foundation Brain Model for Embodied Intelligence
    "https://arxiv.org/abs/2511.00153",  # EgoMI: Learning Active Vision and Whole-Body Manipulation from Egocentric Human Demonstrations
    "https://arxiv.org/abs/2511.00405",  # UME-R1: Exploring Reasoning-Driven Generative Multimodal Embeddings
    "https://arxiv.org/abs/2511.00503",  # Diff4Splat: Controllable 4D Scene Generation with Latent Dynamic Reconstruction Models
    "https://arxiv.org/abs/2511.00511",  # ID-Crafter: VLM-Grounded Online RL for Compositional Multi-Subject Video Generation
    "https://arxiv.org/abs/2511.00609",  # PreferThinker: Reasoning-based Personalized Image Preference Assessment
    "https://arxiv.org/abs/2511.00758",  # Active Thinking Model: A Goal-Directed Self-Improving Framework for Real-World Adaptive Intelligence
    "https://arxiv.org/abs/2511.01107",  # SLAP: Shortcut Learning for Abstract Planning
    "https://arxiv.org/abs/2511.01177",  # Scaling Cross-Embodiment World Models for Dexterous Manipulation
    "https://arxiv.org/abs/2511.01191",  # Self-Harmony: Learning to Harmonize Self-Supervision and Self-Play in Test-Time Reinforcement Learning
    "https://arxiv.org/abs/2511.01294",  # Kinematify: Open-Vocabulary Synthesis of High-DoF Articulated Objects
    "https://arxiv.org/abs/2511.01331",  # RobustVLA: Robustness-Aware Reinforcement Post-Training for Vision-Language-Action Models
    "https://arxiv.org/abs/2511.01571",  # PixelVLA: Advancing Pixel-level Understanding in Vision-Language-Action Model
    "https://arxiv.org/abs/2511.01618",  # Actial: Activate Spatial Reasoning Ability of Multimodal Large Language Models
    "https://arxiv.org/abs/2511.01718",  # Unified Diffusion VLA: Vision-Language-Action Model via Joint Discrete Denoising Diffusion Process
    "https://arxiv.org/abs/2511.01758",  # RLAC: Reinforcement Learning with Adversarial Critic for Free-Form Generation Tasks
    "https://arxiv.org/abs/2511.01833",  # TIR-Bench: A Comprehensive Benchmark for Agentic Thinking-with-Images Reasoning
    "https://arxiv.org/abs/2511.02097",  # A Step Toward World Models: A Survey on Robotic Manipulation
    "https://arxiv.org/abs/2511.02239",  # LACY: A Vision-Language Model-based Language-Action Cycle for Self-Improving Robotic Manipulation
    "https://arxiv.org/abs/2511.02303",  # Unlocking the Power of Multi-Agent LLM for Reasoning: From Lazy Agents to Deliberation
    "https://arxiv.org/abs/2511.02779",  # When Visualizing is the First Step to Reasoning: MIRA, a Benchmark for Visual Chain-of-Thought
    "https://arxiv.org/abs/2511.02824",  # Kosmos: An AI Scientist for Autonomous Discovery
    "https://arxiv.org/abs/2511.02832",  # TWIST2: Scalable, Portable, and Holistic Humanoid Data Collection System
    "https://arxiv.org/abs/2511.03032",  # Leveraging Discrete Function Decomposability for Scientific Design
    "https://arxiv.org/abs/2511.03773",  # Scaling Agent Learning via Experience Synthesis
    "https://arxiv.org/abs/2511.03997",  # PhysCorr: Dual-Reward DPO for Physics-Constrained Text-to-Video Generation with Automated Preference Selection
    "https://arxiv.org/abs/2511.04131",  # BFM-Zero: A Promptable Behavioral Foundation Model for Humanoid Control Using Unsupervised Reinforcement Learning
    "https://arxiv.org/abs/2511.04357",  # GraSP-VLA: Graph-based Symbolic Action Representation for Long-Horizon Planning with VLA Policies
    "https://arxiv.org/abs/2511.04555",  # Evo-1: Lightweight Vision-Language-Action Model with Preserved Semantic Alignment
    "https://arxiv.org/abs/2511.04665",  # Real-to-Sim Robot Policy Evaluation with Gaussian Splatting Simulation of Soft-Body Interactions
    "https://arxiv.org/abs/2511.04670",  # Cambrian-S: Towards Spatial Supersensing in Video
    "https://arxiv.org/abs/2511.04812",  # Multimodal Diffusion Forcing for Forceful Manipulation
    "https://arxiv.org/abs/2511.04831",  # Isaac Lab: A GPU-Accelerated Simulation Framework for Multi-Modal Robot Learning
    "https://arxiv.org/abs/2511.05005",  # Multi-agent Coordination via Flow Matching
    "https://arxiv.org/abs/2511.05271",  # DeepEyesV2: Toward Agentic Multimodal Model
    "https://arxiv.org/abs/2511.05275",  # TwinVLA: Data-Efficient Bimanual Manipulation with Twin Single-Arm Vision-Language-Action Models
    "https://arxiv.org/abs/2511.05489",  # TimeSearch-R: Adaptive Temporal Search for Long-Form Video Understanding via Self-Verification Reinforcement Learning
    "https://arxiv.org/abs/2511.05491",  # Visual Spatial Tuning
    "https://arxiv.org/abs/2511.05849",  # EGG-SR: Embedding Symbolic Equivalence into Symbolic Regression via Equality Graph
    "https://arxiv.org/abs/2511.05936",  # 10 Open Challenges Steering the Future of Vision-Language-Action Models
    "https://arxiv.org/abs/2511.05963",  # Next-Latent Prediction Transformers Learn Compact World Models
    "https://arxiv.org/abs/2511.06281",  # VideoSSR: Video Self-Supervised Reinforcement Learning
    "https://arxiv.org/abs/2511.06299",  # Physics-Informed Deformable Gaussian Splatting: Towards Unified Constitutive Laws for Time-Evolving Material Field
    "https://arxiv.org/abs/2511.06385",  # From Demonstrations to Safe Deployment: Path-Consistent Safety Filtering for Diffusion Policies
    "https://arxiv.org/abs/2511.06411",  # SofT-GRPO: Surpassing Discrete-Token LLM Reinforcement Learning via Gumbel-Reparameterized Soft-Thinking Policy Optimization
    "https://arxiv.org/abs/2511.06499",  # SportR: A Benchmark for Multimodal Large Language Model Reasoning in Sports
    "https://arxiv.org/abs/2511.06908",  # Mono3DVG-EnSD: Enhanced Spatial-aware and Dimension-decoupled Text Encoding for Monocular 3D Visual Grounding
    "https://arxiv.org/abs/2511.07317",  # RLVE: Scaling Up Reinforcement Learning for Language Models with Adaptive Verifiable Environments
    "https://arxiv.org/abs/2511.07327",  # IterResearch: Rethinking Long-Horizon Agents with Interaction Scaling
    "https://arxiv.org/abs/2511.07328",  # Q-RAG: Long Context Multi-step Retrieval via Value-based Embedder Training
    "https://arxiv.org/abs/2511.07332",  # Grounding Computer Use Agents on Human Demonstrations
    "https://arxiv.org/abs/2511.07403",  # SpatialThinker: Reinforcing 3D Reasoning in Multimodal LLMs via Spatial Rewards
    "https://arxiv.org/abs/2511.07407",  # Unified Humanoid Fall-Safety Policy from a Few Demonstrations
    "https://arxiv.org/abs/2511.07416",  # Robot Learning from a Physical World Model
    "https://arxiv.org/abs/2511.07730",  # Multistep Quasimetric Learning for Scalable Goal-conditioned Reinforcement Learning
    "https://arxiv.org/abs/2511.07732",  # ViPRA: Video Prediction for Robot Actions
    "https://arxiv.org/abs/2511.07738",  # From Exploration to Exploitation: A Two-Stage Entropy RLVR Approach for Noise-Tolerant MLLM Training
    "https://arxiv.org/abs/2511.07820",  # SONIC: Supersizing Motion Tracking for Natural Humanoid Whole-Body Control
    "https://arxiv.org/abs/2511.07899",  # Statistically Assuring Safety of Control Systems using Ensembles of Safety Filters and Conformal Prediction
    "https://arxiv.org/abs/2511.08234",  # Beyond Distributions: Geometric Action Control for Continuous Reinforcement Learning
    "https://arxiv.org/abs/2511.08544",  # LeJEPA: Provable and Scalable Self-Supervised Learning Without the Heuristics
    "https://arxiv.org/abs/2511.08577",  # Think-at-Hard: Selective Latent Iterations to Improve Reasoning Language Models
    "https://arxiv.org/abs/2511.08585",  # Simulating the Visual World with Artificial Intelligence: A Roadmap
    "https://arxiv.org/abs/2511.09018",  # Causally-Grounded Dual-Path Attention Intervention for Object Hallucination Mitigation in LVLMs
    "https://arxiv.org/abs/2511.09057",  # PAN: A World Model for General, Interactable, and Long-Horizon World Simulation
    "https://arxiv.org/abs/2511.09158",  # Efficient Reasoning via Reward Model
    "https://arxiv.org/abs/2511.09484",  # SPIDER: Scalable Physics-Informed Dexterous Retargeting
    "https://arxiv.org/abs/2511.09515",  # WMPO: World Model-based Policy Optimization for Vision-Language-Action Models
    "https://arxiv.org/abs/2511.09558",  # IFG: Internet-Scale Guidance for Functional Grasping Generation
    "https://arxiv.org/abs/2511.09602",  # ScaleADFG: Affordance-based Dexterous Functional Grasping via Scalable Dataset
    "https://arxiv.org/abs/2511.09611",  # MMaDA-Parallel: Multimodal Large Diffusion Language Models for Thinking-Aware Editing and Generation
    "https://arxiv.org/abs/2511.09681",  # SEBA: Sample-Efficient Black-Box Attacks on Visual Reinforcement Learning
    "https://arxiv.org/abs/2511.10055",  # Image Aesthetic Reasoning via HCM-GRPO: Empowering Compact Model for Superior Performance
    "https://arxiv.org/abs/2511.10276",  # RoboBenchMart: Benchmarking Robots in Retail Environment
    "https://arxiv.org/abs/2511.10279",  # PROPA: Toward Process-level Optimization in Visual Reasoning via Reinforcement Learning
    "https://arxiv.org/abs/2511.10395",  # AgentEvolver: Towards Efficient Self-Evolving Agent System
    "https://arxiv.org/abs/2511.10560",  # OmniVGGT: Omni-Modality Driven Visual Geometry Grounded Transformer
    "https://arxiv.org/abs/2511.10647",  # Depth Anything 3: Recovering the Visual Space from Any Views
    "https://arxiv.org/abs/2511.10648",  # Enhancing the Outcome Reward-based RL Training of MLLMs with Self-Consistency Sampling
    "https://arxiv.org/abs/2511.10985",  # When Data is the Algorithm: A Systematic Study and Curation of Preference Optimization Datasets
    "https://arxiv.org/abs/2511.11007",  # VisMem: Latent Vision Memory Unlocks Potential of Vision-Language Models
    "https://arxiv.org/abs/2511.11011",  # Efficient Image-Goal Navigation with Representative Latent World Model
    "https://arxiv.org/abs/2511.11113",  # VIDEOP2R: Video Understanding from Perception to Reasoning
    "https://arxiv.org/abs/2511.11478",  # Rethinking Progression of Memory State in Robotic Manipulation: An Object-Centric Perspective
    "https://arxiv.org/abs/2511.11520",  # Scalable Policy Evaluation with Video World Models
    "https://arxiv.org/abs/2511.12149",  # AttackVLA: Benchmarking Adversarial and Backdoor Attacks on Vision-Language-Action Models
    "https://arxiv.org/abs/2511.12882",  # Towards High-Consistency Embodied World Model with Multi-View Trajectory Videos
    "https://arxiv.org/abs/2511.13026",  # REVISOR: Beyond Textual Reflection, Towards Multimodal Introspective Reasoning in Long-Form Video Understanding
    "https://arxiv.org/abs/2511.13054",  # ViSS-R1: Self-Supervised Reinforcement Video Reasoning
    "https://arxiv.org/abs/2511.13648",  # PhysX-Anything: Simulation-Ready Physical 3D Assets from Single Image
    "https://arxiv.org/abs/2511.13720",  # Back to Basics: Let Denoising Generative Models Denoise
    "https://arxiv.org/abs/2511.13787",  # Exploring Transferability of Self-Supervised Learning by Task Conflict Calibration
    "https://arxiv.org/abs/2511.13945",  # Can You Learn to See Without Images? Procedural Warm-Up for Vision Transformers
    "https://arxiv.org/abs/2511.14004",  # Searching in Space and Time: Unified Memory-Action Loops for Open-World Object Retrieval
    "https://arxiv.org/abs/2511.14148",  # AsyncVLA: Asynchronous Flow Matching for Vision-Language-Action Models
    "https://arxiv.org/abs/2511.14565",  # Masked IRL: LLM-Guided Reward Disambiguation from Demonstrations and Language
    "https://arxiv.org/abs/2511.14659",  # NORA-1.5: A Vision-Language-Action Model Trained using World Model- and Action-based Preference Rewards
    "https://arxiv.org/abs/2511.14759",  # $π^{*}_{0.6}$: a VLA That Learns From Experience
    "https://arxiv.org/abs/2511.15190",  # Masked Auto-Regressive Variational Acceleration: Fast Inference Makes Practical Reinforcement Learning
    "https://arxiv.org/abs/2511.15200",  # VIRAL: Visual Sim-to-Real at Scale for Humanoid Loco-Manipulation
    "https://arxiv.org/abs/2511.15407",  # IPR-1: Interactive Physical Reasoner
    "https://arxiv.org/abs/2511.15605",  # SRPO: Self-Referential Policy Optimization for Vision-Language-Action Models
    "https://arxiv.org/abs/2511.15613",  # When to Think and When to Look: Uncertainty-Guided Lookback
    "https://arxiv.org/abs/2511.15622",  # The SA-FARI Dataset: Segment Anything in Footage of Animals for Recognition and Identification
    "https://arxiv.org/abs/2511.15661",  # VisPlay: Self-Evolving Vision-Language Models from Images
    "https://arxiv.org/abs/2511.15703",  # Think Visually, Reason Textually: Vision-Language Synergy in ARC
    "https://arxiv.org/abs/2511.16043",  # Agent0: Unleashing Self-Evolving Agents from Zero Data via Tool-Integrated Reasoning
    "https://arxiv.org/abs/2511.16077",  # VideoSeg-R1:Reasoning Video Object Segmentation via Reinforcement Learning
    "https://arxiv.org/abs/2511.16160",  # Video2Layout: Recall and Reconstruct Metric-Grounded Cognitive Map for Spatial Reasoning
    "https://arxiv.org/abs/2511.16166",  # EvoVLA: Self-Evolving Vision-Language-Action Model
    "https://arxiv.org/abs/2511.16175",  # Mantis: A Versatile Vision-Language-Action Model with Disentangled Visual Foresight
    "https://arxiv.org/abs/2511.16223",  # DynaMimicGen: A Data Generation Framework for Robot Learning of Dynamic Tasks
    "https://arxiv.org/abs/2511.16334",  # OpenMMReasoner: Pushing the Frontiers for Multimodal Reasoning with an Open and General Recipe
    "https://arxiv.org/abs/2511.16407",  # LAOF: Robust Latent Action Learning with Optical Flow Constraints
    "https://arxiv.org/abs/2511.16518",  # MiMo-Embodied: X-Embodied Foundation Model Technical Report
    "https://arxiv.org/abs/2511.16624",  # SAM 3D: 3Dfy Anything in Images
    "https://arxiv.org/abs/2511.16651",  # InternData-A1: Pioneering High-Fidelity Synthetic Data for Pre-training Generalist Policy
    "https://arxiv.org/abs/2511.16652",  # Evolution Strategies at the Hyperscale
    "https://arxiv.org/abs/2511.16669",  # Video-as-Answer: Predict and Generate Next Video Event with Joint-GRPO
    "https://arxiv.org/abs/2511.16671",  # Thinking-while-Generating: Interleaving Textual Reasoning throughout Visual Generation
    "https://arxiv.org/abs/2511.16672",  # EvoLMM: Self-Evolving Large Multimodal Models with Continuous Rewards
    "https://arxiv.org/abs/2511.16674",  # Dataset Distillation for Pre-Trained Self-Supervised Vision Models
    "https://arxiv.org/abs/2511.16886",  # Latent Reasoning in TRMs is Secretly a Policy Improvement Operator
    "https://arxiv.org/abs/2511.17097",  # Progress-Think: Semantic Progress Reasoning for Vision-Language Navigation
    "https://arxiv.org/abs/2511.17171",  # FireScope: Wildfire Risk Raster Prediction with a Chain-of-Thought Oracle
    "https://arxiv.org/abs/2511.17199",  # VLA-4D: Embedding 4D Awareness into Vision-Language-Action Models for SpatioTemporally Coherent Robotic Manipulation
    "https://arxiv.org/abs/2511.17309",  # MuM: Multi-View Masked Image Modeling for 3D Vision
    "https://arxiv.org/abs/2511.17366",  # METIS: Multi-Source Egocentric Training for Integrated Dexterous Vision-Language-Action Model
    "https://arxiv.org/abs/2511.17367",  # R2PS: Worst-Case Robust Real-Time Pursuit Strategies under Partial Observability
    "https://arxiv.org/abs/2511.17441",  # RoboCOIN: An Open-Sourced Bimanual Robotic Data COllection for INtegrated Manipulation
    "https://arxiv.org/abs/2511.17450",  # Planning with Sketch-Guided Verification for Physics-Aware Video Generation
    "https://arxiv.org/abs/2511.17473",  # Masked-and-Reordered Self-Supervision for Reinforcement Learning from Verifiable Rewards
    "https://arxiv.org/abs/2511.17487",  # Downscaling Intelligence: Exploring Perception and Reasoning Bottlenecks in Small Multimodal Models
    "https://arxiv.org/abs/2511.17502",  # RynnVLA-002: A Unified Vision-Language-Action and World Model
    "https://arxiv.org/abs/2511.17879",  # Generative Adversarial Post-Training Mitigates Reward Hacking in Live Human-AI Music Interaction
    "https://arxiv.org/abs/2511.17925",  # Switch-JustDance: Benchmarking Whole Body Motion Tracking Controllers Using a Commercial Console Game
    "https://arxiv.org/abs/2511.18085",  # Continually Evolving Skill Knowledge in Vision Language Action Model
    "https://arxiv.org/abs/2511.18112",  # EchoVLA: Synergistic Declarative Memory for VLA-Driven Mobile Manipulation
    "https://arxiv.org/abs/2511.18305",  # DiVE-k: Differential Visual Reasoning for Fine-grained Image Recognition
    "https://arxiv.org/abs/2511.18373",  # MASS: Motion-Aware Spatial-Temporal Grounding for Physics Reasoning and Comprehension in Vision-Language Models
    "https://arxiv.org/abs/2511.18378",  # Synthetic Curriculum Reinforces Compositional Text-to-Image Generation
    "https://arxiv.org/abs/2511.18424",  # CrossJEPA: Cross-Modal Joint-Embedding Predictive Architecture for Efficient 3D Representation Learning from 2D Images
    "https://arxiv.org/abs/2511.18437",  # Perceptual-Evidence Anchored Reinforced Learning for Multimodal Reasoning
    "https://arxiv.org/abs/2511.18509",  # SafeFall: Learning Protective Control for Humanoid Robots
    "https://arxiv.org/abs/2511.18538",  # From Code Foundation Models to Agents and Applications: A Comprehensive Survey and Practical Guide to Code Intelligence
    "https://arxiv.org/abs/2511.18719",  # Seeing What Matters: Visual Preference Policy Optimization for Visual Generation
    "https://arxiv.org/abs/2511.18810",  # MergeVLA: Cross-Skill Model Merging Toward a Generalist Vision-Language-Action Agent
    "https://arxiv.org/abs/2511.18845",  # UNeMo: Collaborative Visual-Language Reasoning and Navigation via a Multimodal World Model
    "https://arxiv.org/abs/2511.18960",  # AVA-VLA: Improving Vision-Language-Action models with Active Visual Attention
    "https://arxiv.org/abs/2511.19221",  # Percept-WAM: Perception-Enhanced World-Awareness-Action Model for Robust End-to-End Autonomous Driving
    "https://arxiv.org/abs/2511.19261",  # LAST: LeArning to Think in Space and Time for Generalist Vision-Language Models
    "https://arxiv.org/abs/2511.19418",  # Chain-of-Visual-Thought: Teaching VLMs to See and Think Better with Continuous Visual Tokens
    "https://arxiv.org/abs/2511.19524",  # VideoChat-M1: Collaborative Policy Planning for Video Understanding via Multi-Agent Reinforcement Learning
    "https://arxiv.org/abs/2511.19584",  # Learning Massively Multitask World Models for Continuous Control
    "https://arxiv.org/abs/2511.19661",  # CodeV: Code with Images for Faithful Visual Reasoning via Tool-Aware Policy Optimization
    "https://arxiv.org/abs/2511.19684",  # IndEgo: A Dataset of Industrial Scenarios and Collaborative Work for Egocentric Assistants
    "https://arxiv.org/abs/2511.19773",  # Scaling Agentic Reinforcement Learning for Tool-Integrated Reasoning in VLMs
    "https://arxiv.org/abs/2511.19820",  # CropVLM: Learning to Zoom for Fine-Grained Vision-Language Perception
    "https://arxiv.org/abs/2511.19859",  # Unifying Perception and Action: A Hybrid-Modality Pipeline with Implicit Visual Chain-of-Thought for Robotic Action Generation
    "https://arxiv.org/abs/2511.19861",  # GigaWorld-0: World Models as Data Engine to Empower Embodied AI
    "https://arxiv.org/abs/2511.19878",  # MAPS: Preserving Vision-Language Representations via Module-Wise Proximity Scheduling for Better Vision-Language-Action Generalization
    "https://arxiv.org/abs/2511.19900",  # Agent0-VL: Exploring Self-Evolving Agent for Tool-Integrated Vision-Language Reasoning
    "https://arxiv.org/abs/2511.19965",  # HiCoGen: Hierarchical Compositional Text-to-Image Generation in Diffusion Models via Reinforcement Learning
    "https://arxiv.org/abs/2511.19972",  # Boosting Reasoning in Large Multimodal Models via Activation Replay
    "https://arxiv.org/abs/2511.20085",  # VICoT-Agent: A Vision-Interleaved Chain-of-Thought Framework for Interpretable Multimodal Reasoning and Scalable Remote Sensing Analysis
    "https://arxiv.org/abs/2511.20256",  # The Image as Its Own Reward: Reinforcement Learning with Adversarial Reward for Image Generation
    "https://arxiv.org/abs/2511.20275",  # HAFO: A Force-Adaptive Control Framework for Humanoid Robots in Intense Interaction Environments
    "https://arxiv.org/abs/2511.20280",  # Bootstrapping Physics-Grounded Video Generation through VLM-Guided Iterative Self-Refinement
    "https://arxiv.org/abs/2511.20348",  # Material-informed Gaussian Splatting for 3D World Reconstruction in a Digital Twin
    "https://arxiv.org/abs/2511.20351",  # Thinking in 360°: Humanoid Visual Search in the Wild
    "https://arxiv.org/abs/2511.20549",  # Flash-DMD: Towards High-Fidelity Few-Step Image Generation with Efficient Distillation and Joint Reinforcement Learning
    "https://arxiv.org/abs/2511.20629",  # MapReduce LoRA: Advancing the Pareto Front in Multi-Preference Optimization for Generative Models
    "https://arxiv.org/abs/2511.20639",  # Latent Collaboration in Multi-Agent Systems
    "https://arxiv.org/abs/2511.20645",  # PixelDiT: Pixel Diffusion Transformers for Image Generation
    "https://arxiv.org/abs/2511.20785",  # LongVT: Incentivizing "Thinking with Long Videos" via Native Tool Calling
    "https://arxiv.org/abs/2511.20814",  # SPHINX: A Synthetic Environment for Visual Perception and Reasoning
    "https://arxiv.org/abs/2511.20836",  # Structured Prompting Enables More Robust Evaluation of Language Models
    "https://arxiv.org/abs/2511.20844",  # Pre-train to Gain: Robust Learning Without Clean Labels
    "https://arxiv.org/abs/2511.20886",  # V$^{2}$-SAM: Marrying SAM2 with Multi-Prompt Experts for Cross-View Object Correspondence
    "https://arxiv.org/abs/2511.20937",  # ENACT: Evaluating Embodied Cognition with World Modeling of Egocentric Interaction
    "https://arxiv.org/abs/2511.21083",  # Dual-Agent Reinforcement Learning for Adaptive and Cost-Aware Visual-Inertial Odometry
    "https://arxiv.org/abs/2511.21135",  # SocialNav: Training Human-Inspired Foundation Model for Socially-Aware Embodied Navigation
    "https://arxiv.org/abs/2511.21169",  # Kinematics-Aware Multi-Policy Reinforcement Learning for Force-Capable Humanoid Loco-Manipulation
    "https://arxiv.org/abs/2511.21192",  # When Robots Obey the Patch: Universal Transferable Patch Attacks on Vision-Language-Action Models
    "https://arxiv.org/abs/2511.21264",  # Sampling-Based Optimization with Parallelized Physics Simulator for Bimanual Manipulation
    "https://arxiv.org/abs/2511.21395",  # Monet: Reasoning in Latent Visual Space Beyond Images and Language
    "https://arxiv.org/abs/2511.21428",  # From Observation to Action: Latent Action-based Primitive Segmentation for VLA Pre-training in Industrial Settings
    "https://arxiv.org/abs/2511.21471",  # SpatialBench: Benchmarking Multimodal Large Language Models for Spatial Cognition
    "https://arxiv.org/abs/2511.21688",  # G$^2$VLM: Geometry Grounded Vision Language Model with Unified 3D Reconstruction and Spatial Reasoning
    "https://arxiv.org/abs/2511.21887",  # UniArt: Unified 3D Representation for Generating 3D Articulated Objects with Open-Set Articulation
    "https://arxiv.org/abs/2511.22235",  # Training High-Level Schedulers with Execution-Feedback Reinforcement Learning for Long-Horizon GUI Automation
    "https://arxiv.org/abs/2511.22555",  # Beyond Success: Refining Elegant Robot Manipulation from Mixed-Quality Data via Just-in-Time Intervention
    "https://arxiv.org/abs/2511.22715",  # ReAG: Reasoning-Augmented Generation for Knowledge-based Visual Question Answering
    "https://arxiv.org/abs/2511.22780",  # Distracted Robot: How Visual Clutter Undermine Robotic Manipulation
    "https://arxiv.org/abs/2511.22950",  # RobotSeg: A Model and Dataset for Segmenting Robots in Image and Video
    "https://arxiv.org/abs/2511.22989",  # MultiBanana: A Challenging Benchmark for Multi-Reference Text-to-Image Generation
    "https://arxiv.org/abs/2511.23369",  # SimScale: Learning to Drive via Real-World Simulation at Scale
    "https://arxiv.org/abs/2512.00076",  # Arcadia: Toward a Full-Lifecycle Framework for Embodied Lifelong Learning
    "https://arxiv.org/abs/2512.00425",  # What about gravity in video generation? Post-Training Newton's Laws with Verifiable Rewards
    "https://arxiv.org/abs/2512.00489",  # Learning What Helps: Task-Aligned Context Selection for Vision Tasks
    "https://arxiv.org/abs/2512.00536",  # Algorithmic Guarantees for Distilling Supervised and Offline RL Datasets
    "https://arxiv.org/abs/2512.00805",  # Thinking with Drafts: Speculative Temporal Reasoning for Efficient Long Video Understanding
    "https://arxiv.org/abs/2512.00836",  # Assessing model error in counterfactual worlds
    "https://arxiv.org/abs/2512.00903",  # SwiftVLA: Unlocking Spatiotemporal Dynamics for Lightweight VLA Models at Minimal Overhead
    "https://arxiv.org/abs/2512.00915",  # Partially Equivariant Reinforcement Learning in Symmetry-Breaking Environments
    "https://arxiv.org/abs/2512.00961",  # Goal-Driven Reward by Video Diffusion Models for Reinforcement Learning
    "https://arxiv.org/abs/2512.00971",  # H-Zero: Cross-Humanoid Locomotion Pretraining Enables Few-shot Novel Embodiment Transfer
    "https://arxiv.org/abs/2512.00975",  # MM-ACT: Learn from Multimodal Parallel Generation to Act
    "https://arxiv.org/abs/2512.01047",  # Automating the Refinement of Reinforcement Learning Specifications
    "https://arxiv.org/abs/2512.01061",  # Opening the Sim-to-Real Door for Humanoid Pixel-to-Action Policy Transfer
    "https://arxiv.org/abs/2512.01119",  # World Model Robustness via Surprise Recognition
    "https://arxiv.org/abs/2512.01127",  # Mode-Conditioning Unlocks Superior Test-Time Scaling
    "https://arxiv.org/abs/2512.01228",  # On the Tension Between Optimality and Adversarial Robustness in Policy Optimization
    "https://arxiv.org/abs/2512.01236",  # PSR: Scaling Multi-Subject Personalized Image Generation with Pairwise Subject-Consistency Rewards
    "https://arxiv.org/abs/2512.01342",  # InternVideo-Next: Towards General Video Foundation Models without Video-Text Supervision
    "https://arxiv.org/abs/2512.01374",  # Stabilizing Reinforcement Learning with LLMs: Formulation and Practices
    "https://arxiv.org/abs/2512.01550",  # NavForesee: A Unified Vision-Language World Model for Hierarchical Planning and Dual-Horizon Navigation Prediction
    "https://arxiv.org/abs/2512.01643",  # ViT$^3$: Unlocking Test-Time Training in Vision
    "https://arxiv.org/abs/2512.01738",  # MSPT: Efficient Large-Scale Physical Modeling via Parallelized Multi-Scale Attention
    "https://arxiv.org/abs/2512.01925",  # Rectifying LLM Thought from Lens of Optimization
    "https://arxiv.org/abs/2512.01946",  # Scaling Cross-Environment Failure Reasoning Data for Vision-Language Robotic Manipulation
    "https://arxiv.org/abs/2512.01989",  # PAI-Bench: A Comprehensive Benchmark For Physical AI
    "https://arxiv.org/abs/2512.01996",  # Learning Sim-to-Real Humanoid Locomotion in 15 Minutes
    "https://arxiv.org/abs/2512.02389",  # Synthetic Error Injection Fails to Elicit Self-Correction In Language Models
    "https://arxiv.org/abs/2512.02472",  # Guided Self-Evolving LLMs with Minimal Human Supervision
    "https://arxiv.org/abs/2512.02486",  # Dual-Robust Cross-Domain Offline Reinforcement Learning Against Dynamics Shifts
    "https://arxiv.org/abs/2512.02729",  # RoboWheel: A Data Engine from Real-World Human Demonstrations for Cross-Embodiment Robotic Learning
    "https://arxiv.org/abs/2512.02787",  # Diagnose, Correct, and Learn from Manipulation Failures via Visual Symbols
    "https://arxiv.org/abs/2512.02834",  # Steering Vision-Language-Action Models as Anti-Exploration: A Test-Time Scaling Approach
    "https://arxiv.org/abs/2512.02851",  # SwarmDiffusion: End-To-End Traversability-Guided Diffusion for Embodiment-Agnostic Navigation of Heterogeneous Robots
    "https://arxiv.org/abs/2512.02902",  # VLA Models Are More Generalizable Than You Think: Revisiting Physical and Spatial Modeling
    "https://arxiv.org/abs/2512.03043",  # OneThinker: All-in-one Reasoning Model for Image and Video
    "https://arxiv.org/abs/2512.03126",  # Hierarchical Process Reward Models are Symbolic Vision Learners
    "https://arxiv.org/abs/2512.03422",  # What Is The Best 3D Scene Representation for Robotics? From Geometric to Foundation Models
    "https://arxiv.org/abs/2512.03442",  # PretrainZero: Reinforcement Active Pretraining
    "https://arxiv.org/abs/2512.03556",  # RoboScape-R: Unified Reward-Observation World Models for Generalizable Robotics Training via RL
    "https://arxiv.org/abs/2512.03707",  # ContactRL: Safe Reinforcement Learning based Motion Planning for Contact based Human Robot Collaboration
    "https://arxiv.org/abs/2512.03743",  # House of Dextra: Cross-embodied Co-design for Dexterous Hands
    "https://arxiv.org/abs/2512.03746",  # Thinking with Programming Vision: Towards a Unified View for Thinking with Images
    "https://arxiv.org/abs/2512.03759",  # Principled RL for Diffusion LLMs Emerges from a Sequence-Level Perspective
    "https://arxiv.org/abs/2512.03794",  # AdaptVision: Efficient Vision-Language Models via Adaptive Visual Acquisition
    "https://arxiv.org/abs/2512.03874",  # OmniDexVLG: Learning Dexterous Grasp Generation from Vision Language Model-Guided Grasp Semantics, Taxonomy and Functional Affordance
    "https://arxiv.org/abs/2512.03913",  # Hierarchical Vision Language Action Model Using Success and Failure Demonstrations
    "https://arxiv.org/abs/2512.03963",  # TempR1: Improving Temporal Understanding of MLLMs via Temporal-Aware Multi-Task Reinforcement Learning
    "https://arxiv.org/abs/2512.03973",  # Guided Flow Policy: Learning from High-Value Actions in Offline Reinforcement Learning
    "https://arxiv.org/abs/2512.04012",  # Emergent Outlier View Rejection in Visual Geometry Grounded Transformers
    "https://arxiv.org/abs/2512.04040",  # RELIC: Interactive Video World Model with Long-Horizon Memory
    "https://arxiv.org/abs/2512.04069",  # SpaceTools: Tool-Augmented Spatial Reasoning via Double Interactive RL
    "https://arxiv.org/abs/2512.04072",  # SkillFactory: Self-Distillation For Learning Cognitive Behaviors
    "https://arxiv.org/abs/2512.04221",  # MoReGen: Multi-Agent Motion-Reasoning Engine for Code-based Text-to-Video Synthesis
    "https://arxiv.org/abs/2512.04381",  # FALCON: Actively Decoupled Visuomotor Policies for Loco-Manipulation with Foundation-Model-Based Coordination
    "https://arxiv.org/abs/2512.04388",  # Learning to Orchestrate Agents in Natural Language with the Conductor
    "https://arxiv.org/abs/2512.04563",  # COOPER: A Unified Model for Cooperative Perception and Reasoning in Spatial Intelligence
    "https://arxiv.org/abs/2512.04731",  # Bridging Simulation and Reality: Cross-Domain Transfer with Semantic 2D Gaussian Splatting
    "https://arxiv.org/abs/2512.04733",  # E3AD: An Emotion-Aware Vision-Language-Action Model for Human-Centric End-to-End Autonomous Driving
    "https://arxiv.org/abs/2512.04784",  # PaCo-RL: Advancing Reinforcement Learning for Consistent Image Generation with Pairwise Reward Modeling
    "https://arxiv.org/abs/2512.04884",  # Hoi! - A Multimodal Dataset for Force-Grounded, Cross-View Articulated Manipulation
    "https://arxiv.org/abs/2512.04952",  # FASTer: Toward Efficient Autoregressive Vision Language Action Modeling via Neural Action Tokenization
    "https://arxiv.org/abs/2512.05024",  # Model-Free Assessment of Simulator Fidelity via Quantile Curves
    "https://arxiv.org/abs/2512.05094",  # From Generated Human Videos to Physically Plausible Robot Trajectories
    "https://arxiv.org/abs/2512.05111",  # ARM-Thinker: Reinforcing Multimodal Generative Reward Models with Agentic Tool Use and Visual Reasoning
    "https://arxiv.org/abs/2512.05356",  # AI & Human Co-Improvement for Safer Co-Superintelligence
    "https://arxiv.org/abs/2512.05564",  # ProPhy: Progressive Physical Alignment for Dynamic World Simulation
    "https://arxiv.org/abs/2512.05665",  # Interleaved Latent Visual Reasoning with Selective Perceptual Modeling
    "https://arxiv.org/abs/2512.05955",  # SIMPACT: Simulation-Enabled Action Planning using Vision-Language Models
    "https://arxiv.org/abs/2512.05962",  # Whatever Remains Must Be True: Filtering Drives Reasoning in LLMs, Shaping Diversity
    "https://arxiv.org/abs/2512.06104",  # ARC-AGI Without Pretraining
    "https://arxiv.org/abs/2512.06112",  # WAM-Flow: Parallel Coarse-to-Fine Motion Planning via Discrete Flow Matching for Autonomous Driving
    "https://arxiv.org/abs/2512.06281",  # Unleashing the Intrinsic Visual Representation Capability of Multimodal Large Language Models
    "https://arxiv.org/abs/2512.06628",  # MIND-V: Hierarchical World Model for Long-Horizon Robotic Manipulation with RL-based Physical Alignment
    "https://arxiv.org/abs/2512.06674",  # RunawayEvil: Jailbreaking the Image-to-Video Generative Models
    "https://arxiv.org/abs/2512.06810",  # MMDuet2: Enhancing Proactive Interaction of Video MLLMs with Multi-Turn Reinforcement Learning
    "https://arxiv.org/abs/2512.06835",  # Decouple to Generalize: Context-First Self-Evolving Learning for Data-Scarce Vision-Language Reasoning
    "https://arxiv.org/abs/2512.06963",  # VideoVLA: Video Generators Can Be Generalizable Robot Manipulators
    "https://arxiv.org/abs/2512.07203",  # MMRPT: MultiModal Reinforcement Pre-Training via Masked Vision-Dependent Reasoning
    "https://arxiv.org/abs/2512.07248",  # Distinguishing Imitation Error from Intrinsic Motion Learning Difficulty
    "https://arxiv.org/abs/2512.07464",  # Gait-Adaptive Perceptive Humanoid Locomotion with Real-Time Under-Base Terrain Reconstruction
    "https://arxiv.org/abs/2512.07472",  # Affordance Field Intervention: Enabling VLAs to Escape Memory Traps in Robotic Manipulation
    "https://arxiv.org/abs/2512.07558",  # ReLaX: Reasoning with Latent Exploration for Large Reasoning Models
    "https://arxiv.org/abs/2512.07733",  # SpatialDreamer: Incentivizing Spatial Reasoning via Active Mental Imagery
    "https://arxiv.org/abs/2512.08108",  # Scalable Offline Model-Based RL with Action Chunks
    "https://arxiv.org/abs/2512.08153",  # TreeGRPO: Tree-Advantage GRPO for Online RL Post-Training of Diffusion Models
    "https://arxiv.org/abs/2512.08228",  # MM-CoT:A Benchmark for Probing Visual Chain-of-Thought Reasoning in Multimodal Models
    "https://arxiv.org/abs/2512.08269",  # EgoX: Egocentric Video Generation from a Single Exocentric Video
    "https://arxiv.org/abs/2512.08333",  # Robust Finetuning of Vision-Language-Action Robot Policies via Parameter Merging
    "https://arxiv.org/abs/2512.08411",  # Prismatic World Model: Learning Compositional Dynamics for Planning in Hybrid Systems
    "https://arxiv.org/abs/2512.08511",  # Thinking with Images via Self-Calling Agent
    "https://arxiv.org/abs/2512.08889",  # No Labels, No Problem: Training Visual Reasoners with Multimodal Verifiers
    "https://arxiv.org/abs/2512.08924",  # Efficiently Reconstructing Dynamic Scenes One D4RT at a Time
    "https://arxiv.org/abs/2512.09297",  # One-Shot Real-World Demonstration Synthesis for Scalable Bimanual Manipulation
    "https://arxiv.org/abs/2512.09322",  # Self-Supervised Learning with Gaussian Processes
    "https://arxiv.org/abs/2512.09441",  # Representation Calibration and Uncertainty Guidance for Class-Incremental Learning based on Vision Language Model
    "https://arxiv.org/abs/2512.09706",  # Training One Model to Master Cross-Level Agentic Actions via Reinforcement Learning
    "https://arxiv.org/abs/2512.09924",  # ReViSE: Towards Reason-Informed Video Editing in Unified Models with Self-Reflective Learning
    "https://arxiv.org/abs/2512.09928",  # HiF-VLA: Hindsight, Insight and Foresight through Motion Representation for Vision-Language-Action Models
    "https://arxiv.org/abs/2512.09929",  # Closing the Train-Test Gap in World Models for Gradient-Based Planning
    "https://arxiv.org/abs/2512.10359",  # Tool-Augmented Spatiotemporal Reasoning for Streamlining Video Question Answering Task
    "https://arxiv.org/abs/2512.10534",  # Achieving Olympia-Level Geometry Large Language Model Agent via Complexity Boosting Reinforcement Learning
    "https://arxiv.org/abs/2512.10554",  # Grounding Everything in Tokens for Multimodal Large Language Models
    "https://arxiv.org/abs/2512.10675",  # Evaluating Gemini Robotics Policies in a Veo World Simulator
    "https://arxiv.org/abs/2512.10863",  # MMSI-Video-Bench: A Holistic Benchmark for Video-Based Spatial Intelligence
    "https://arxiv.org/abs/2512.10927",  # FoundationMotion: Auto-Labeling and Reasoning about Spatial Movement in Videos
    "https://arxiv.org/abs/2512.10938",  # Stronger Normalization-Free Transformers
    "https://arxiv.org/abs/2512.10942",  # VL-JEPA: Joint Embedding Predictive Architecture for Vision-language
    "https://arxiv.org/abs/2512.10949",  # Are We Ready for RL in Text-to-3D Generation? A Progressive Investigation
    "https://arxiv.org/abs/2512.10950",  # E-RayZer: Self-supervised 3D Reconstruction as Spatial Visual Pre-training
    "https://arxiv.org/abs/2512.10958",  # WorldLens: Full-Spectrum Evaluations of Driving World Models in Real World
    "https://arxiv.org/abs/2512.11047",  # WholeBodyVLA: Towards Unified Latent VLA for Whole-Body Loco-Manipulation Control
    "https://arxiv.org/abs/2512.11061",  # VDAWorld: World Modelling via VLM-Directed Abstraction and Simulation
    "https://arxiv.org/abs/2512.11114",  # In-Context Multi-Objective Optimization
    "https://arxiv.org/abs/2512.11141",  # Learning complete and explainable visual representations from itemized text supervision
    "https://arxiv.org/abs/2512.11391",  # Mitigating the Safety Alignment Tax with Null-Space Constrained Policy Optimization
    "https://arxiv.org/abs/2512.11782",  # MatAnyone 2: Scaling Video Matting via a Learned Quality Evaluator
    "https://arxiv.org/abs/2512.11797",  # AnchorDream: Repurposing Video Diffusion for Embodiment-Aware Robot Data Synthesis
    "https://arxiv.org/abs/2512.11891",  # VLSA: Vision-Language-Action Models with Plug-and-Play Safety Constraint Layer
    "https://arxiv.org/abs/2512.11908",  # Safe Learning for Contact-Rich Robot Tasks: A Survey from Classical Learning-Based Methods to Safe Foundation Models
    "https://arxiv.org/abs/2512.12046",  # Goal Reaching with Eikonal-Constrained Hierarchical Quasimetric Reinforcement Learning
    "https://arxiv.org/abs/2512.12230",  # Learning to Get Up Across Morphologies: Zero-Shot Recovery with a Unified Humanoid Policy
    "https://arxiv.org/abs/2512.12623",  # Reasoning Within the Mind: Dynamic Multimodal Interleaving in Latent Space
    "https://arxiv.org/abs/2512.12633",  # DiG: Differential Grounding for Enhancing Fine-Grained Perception in Multimodal Large Language Model
    "https://arxiv.org/abs/2512.12690",  # Reassessing the Role of Supervised Fine-Tuning: An Empirical Study in VLM Reasoning
    "https://arxiv.org/abs/2512.12756",  # FysicsWorld: A Unified Full-Modality Benchmark for Any-to-Any Understanding, Generation, and Reasoning
    "https://arxiv.org/abs/2512.12799",  # DrivePI: Spatial-aware 4D MLLM for Unified Autonomous Driving Understanding, Perception, Prediction and Planning
    "https://arxiv.org/abs/2512.12822",  # Lemon: A Unified and Scalable 3D Multimodal Model for Universal Spatial Understanding
    "https://arxiv.org/abs/2512.13030",  # Motus: A Unified Latent Action World Model
    "https://arxiv.org/abs/2512.13043",  # GTR-Turbo: Merged Checkpoint is Secretly a Free Teacher for Agentic VLM Training
    "https://arxiv.org/abs/2512.13080",  # Spatial-Aware VLA Pretraining through Visual-Physical Alignment from Human Videos
    "https://arxiv.org/abs/2512.13093",  # PvP: Data-Efficient Humanoid Robot Learning with Proprioceptive-Privileged Contrastive Representations
    "https://arxiv.org/abs/2512.13106",  # TraPO: A Semi-Supervised Reinforcement Learning Framework for Boosting LLM Reasoning
    "https://arxiv.org/abs/2512.13214",  # Differentiable Material Point Method for the Control of Deformable Objects
    "https://arxiv.org/abs/2512.13564",  # Memory in the Age of AI Agents
    "https://arxiv.org/abs/2512.13592",  # Image Diffusion Preview with Consistency Solver
    "https://arxiv.org/abs/2512.13607",  # Nemotron-Cascade: Scaling Cascaded Reinforcement Learning for General-Purpose Reasoning Models
    "https://arxiv.org/abs/2512.13644",  # World Models Can Leverage Human Videos for Dexterous Manipulation
    "https://arxiv.org/abs/2512.13660",  # RoboTracer: Mastering Spatial Trace with Reasoning in Vision-Language Models for Robotics
    "https://arxiv.org/abs/2512.13683",  # I-Scene: 3D Instance Models are Implicit Generalizable Spatial Learners
    "https://arxiv.org/abs/2512.14202",  # Understanding and Improving Hyperbolic Deep Reinforcement Learning
    "https://arxiv.org/abs/2512.14666",  # EVOLVE-VLA: Test-Time Training from Environment Feedback for Vision-Language-Action Models
    "https://arxiv.org/abs/2512.14692",  # Native and Compact Structured Latents for 3D Generation
    "https://arxiv.org/abs/2512.14693",  # Universal Reasoning Model
    "https://arxiv.org/abs/2512.14696",  # CRISP: Contact-Guided Real2Sim from Monocular Video with Planar Scene Primitives
    "https://arxiv.org/abs/2512.14698",  # TimeLens: Rethinking Video Temporal Grounding with Multimodal LLMs
    "https://arxiv.org/abs/2512.15160",  # EagleVision: A Dual-Stage Framework with BEV-grounding-based Chain-of-Thought for Spatial Intelligence
    "https://arxiv.org/abs/2512.15405",  # EUBRL: Epistemic Uncertainty Directed Bayesian Reinforcement Learning
    "https://arxiv.org/abs/2512.15687",  # Can LLMs Guide Their Own Exploration? Gradient-Guided Reinforcement Learning for LLM Reasoning
    "https://arxiv.org/abs/2512.15692",  # mimic-video: Video-Action Models for Generalizable Robot Control Beyond VLAs
    "https://arxiv.org/abs/2512.15840",  # Large Video Planner Enables Generalizable Robot Control
    "https://arxiv.org/abs/2512.15885",  # Seeing Beyond Words: Self-Supervised Visual Learning for Multimodal Large Language Models
    "https://arxiv.org/abs/2512.15926",  # DSO: Direct Steering Optimization for Bias Mitigation
    "https://arxiv.org/abs/2512.15934",  # In-Context Semi-Supervised Learning
    "https://arxiv.org/abs/2512.16023",  # CoVAR: Co-generation of Video and Action for Robotic Manipulation via Multi-Modal Diffusion
    "https://arxiv.org/abs/2512.16301",  # Adaptation of Agentic AI
    "https://arxiv.org/abs/2512.16584",  # Sketch-in-Latents: Eliciting Unified Reasoning in MLLMs
    "https://arxiv.org/abs/2512.16626",  # Stackelberg Learning from Human Feedback: Preference Optimization as a Sequential Game
    "https://arxiv.org/abs/2512.16649",  # JustRL: Scaling a 1.5B LLM with a Simple RL Recipe
    "https://arxiv.org/abs/2512.16811",  # GeoPredict: Leveraging Predictive Kinematics and 3D Gaussian Geometry for Precise VLA Manipulation
    "https://arxiv.org/abs/2512.16848",  # Meta-RL Induces Exploration in Language Agents
    "https://arxiv.org/abs/2512.16861",  # ReinforceGen: Hybrid Skill Policies with Automated Data Generation and Reinforcement Learning
    "https://arxiv.org/abs/2512.16881",  # PolaRiS: Scalable Real-to-Sim Evaluations for Generalist Robot Policies
    "https://arxiv.org/abs/2512.16899",  # Multimodal RewardBench 2: Evaluating Omni Reward Models for Interleaved Text and Image
    "https://arxiv.org/abs/2512.16909",  # MomaGraph: State-Aware Unified Scene Graphs with Vision-Language Model for Embodied Task Planning
    "https://arxiv.org/abs/2512.16912",  # Exploration vs Exploitation: Rethinking RLVR through Clipping, Entropy, and Spurious Reward
    "https://arxiv.org/abs/2512.16913",  # Depth Any Panoramas: A Foundation Model for Panoramic Depth Estimation
    "https://arxiv.org/abs/2512.16917",  # Generative Adversarial Reasoner: Enhancing LLM Reasoning with Adversarial Reinforcement Learning
    "https://arxiv.org/abs/2512.16918",  # AdaTooler-V: Adaptive Tool-Use for Images and Videos
    "https://arxiv.org/abs/2512.16921",  # Differences That Matter: Auditing Models for Capability Gap Discovery and Rectification
    "https://arxiv.org/abs/2512.16922",  # Next-Embedding Prediction Makes Strong Vision Learners
    "https://arxiv.org/abs/2512.17012",  # 4D-RGPT: Toward Region-level 4D Understanding via Perceptual Distillation
    "https://arxiv.org/abs/2512.17206",  # Reasoning Palette: Modulating Reasoning via Latent Contextualization for Controllable Exploration for (V)LMs
    "https://arxiv.org/abs/2512.17312",  # CodeDance: A Dynamic Tool-integrated MLLM for Executable Visual Reasoning
    "https://arxiv.org/abs/2512.17636",  # Trust-Region Adaptive Policy Optimization
    "https://arxiv.org/abs/2512.18215",  # Stable and Efficient Single-Rollout RL for Multimodal Reasoning
    "https://arxiv.org/abs/2512.18552",  # Toward Training Superintelligent Software Agents through Self-Play SWE-RL
    "https://arxiv.org/abs/2512.18745",  # InSight-o3: Empowering Multimodal Foundation Models with Generalized Visual Search
    "https://arxiv.org/abs/2512.18766",  # MaskFocus: Focusing Policy Optimization on Critical Steps for Masked Image Generation
    "https://arxiv.org/abs/2512.18857",  # CORE: Concept-Oriented Reinforcement for Bridging the Definition-Application Gap in Mathematical Reasoning
    "https://arxiv.org/abs/2512.19133",  # WorldRFT: Latent World Model Planning with Reinforcement Fine-Tuning for Autonomous Driving
    "https://arxiv.org/abs/2512.19154",  # Beyond Sliding Windows: Learning to Manage Memory in Non-Markovian Environments
    "https://arxiv.org/abs/2512.19390",  # TwinAligner: Visual-Dynamic Alignment Empowers Physics-aware Real2Sim2Real for Robotic Manipulation
    "https://arxiv.org/abs/2512.19526",  # QuantiPhy: A Quantitative Benchmark Evaluating Physical Reasoning Abilities of Vision-Language Models
    "https://arxiv.org/abs/2512.19554",  # CARE What Fails: Contrastive Anchored-REflection for Verifiable Multimodal Reasoning
    "https://arxiv.org/abs/2512.19562",  # REALM: A Real-to-Sim Validated Benchmark for Generalization in Robotic Manipulation
    "https://arxiv.org/abs/2512.19605",  # KerJEPA: Kernel Discrepancies for Euclidean Self-Supervised Learning
    "https://arxiv.org/abs/2512.19683",  # From Indoor to Open World: Revealing the Spatial Reasoning Gap in MLLMs
    "https://arxiv.org/abs/2512.19693",  # The Prism Hypothesis: Harmonizing Semantic and Pixel Representations via Unified Autoencoding
    "https://arxiv.org/abs/2512.20092",  # Memory-T1: Reinforcement Learning for Temporal Reasoning in Multi-session Agents
    "https://arxiv.org/abs/2512.20188",  # Asynchronous Fast-Slow Vision-Language-Action Policies for Whole-Body Robotic Manipulation
    "https://arxiv.org/abs/2512.20276",  # ActionFlow: A Pipelined Action Acceleration for Vision Language Models on Edge
    "https://arxiv.org/abs/2512.20605",  # Emergent temporal abstractions in autoregressive models enable hierarchical reinforcement learning
    "https://arxiv.org/abs/2512.20617",  # SpatialTree: How Spatial Abilities Branch Out in MLLMs
    "https://arxiv.org/abs/2512.20675",  # Revisiting the Learning Objectives of Vision-Language Reward Models
    "https://arxiv.org/abs/2512.20745",  # AgentMath: Empowering Mathematical Reasoning for Large Language Models via Tool-Augmented Agent
    "https://arxiv.org/abs/2512.20760",  # Generalization of RLVR Using Causal Reasoning as a Testbed
    "https://arxiv.org/abs/2512.20856",  # NVIDIA Nemotron 3: Efficient and Open Intelligence
    "https://arxiv.org/abs/2512.21218",  # Latent Implicit Visual Reasoning
    "https://arxiv.org/abs/2512.21430",  # EVE: A Generator-Verifier System for Generative Policies
    "https://arxiv.org/abs/2512.21514",  # DiverseGRPO: Mitigating Mode Collapse in Image Generation via Diversity-Aware GRPO
    "https://arxiv.org/abs/2512.21714",  # AstraNav-World: World Model for Foresight Control and Consistency
    "https://arxiv.org/abs/2512.21919",  # SWE-RM: Execution-free Feedback For Software Engineering Agents
    "https://arxiv.org/abs/2512.22238",  # Masking Teacher and Reinforcing Student for Distilling Vision-Language Models
    "https://arxiv.org/abs/2512.22315",  # VideoZoomer: Reinforcement-Learned Temporal Focusing for Long Video Reasoning
    "https://arxiv.org/abs/2512.22414",  # Emergence of Human to Robot Transfer in Vision-Language-Action Models
    "https://arxiv.org/abs/2512.22539",  # VLA-Arena: An Open-Source Framework for Benchmarking Vision-Language-Action Models
    "https://arxiv.org/abs/2512.22545",  # Self-Rewarded Multimodal Coherent Reasoning Across Diverse Visual Domains
    "https://arxiv.org/abs/2512.22647",  # FinPercep-RM: A Fine-grained Reward Model and Co-evolutionary Curriculum for RL-based Real-world Super-Resolution
    "https://arxiv.org/abs/2512.22688",  # Autoregressive Flow Matching for Motion Prediction
    "https://arxiv.org/abs/2512.22799",  # VPTracker: Global Vision-Language Tracking via Visual Prompt and MLLM
    "https://arxiv.org/abs/2512.22939",  # ColaVLA: Leveraging Cognitive Latent Reasoning for Hierarchical Parallel Trajectory Planning in Autonomous Driving
    "https://arxiv.org/abs/2512.23017",  # Merge before Forget: A Single LoRA Continual Learning via Continual Merging
    "https://arxiv.org/abs/2512.23165",  # Evaluating Parameter Efficient Methods for RLVR
    "https://arxiv.org/abs/2512.23167",  # SPIRAL: Symbolic LLM Planning via Grounded and Reflective Search
    "https://arxiv.org/abs/2512.23169",  # REVEALER: Reinforcement-Guided Visual Reasoning for Element-Level Text-Image Alignment Evaluation
    "https://arxiv.org/abs/2512.23333",  # CME-CAD: Heterogeneous Collaborative Multi-Expert Reinforcement Learning for CAD Code Generation
    "https://arxiv.org/abs/2512.23365",  # SpatialMosaic: A Multiview VLM Dataset for Partial Visibility
    "https://arxiv.org/abs/2512.23453",  # CoFi-Dec: Hallucination-Resistant Decoding via Coarse-to-Fine Generative Feedback in Large Vision-Language Models
    "https://arxiv.org/abs/2512.23461",  # Eliminating Inductive Bias in Reward Models with Information-Theoretic Guidance
    "https://arxiv.org/abs/2512.23541",  # Act2Goal: From World Model To General Goal-conditioned Policy
    "https://arxiv.org/abs/2512.23568",  # ThinkGen: Generalized Thinking for Visual Generation
    "https://arxiv.org/abs/2512.23676",  # Web World Models
    "https://arxiv.org/abs/2512.23864",  # Learning to Feel the Future: DreamTacVLA for Contact-Rich Manipulation
    "https://arxiv.org/abs/2512.24119",  # GeoBench: Rethinking Multimodal Geometric Problem-Solving via Hierarchical Evaluation
    "https://arxiv.org/abs/2512.24125",  # Unified Embodied VLM Reasoning with Robotic Action via Autoregressive Discretized Pre-training
    "https://arxiv.org/abs/2512.24146",  # Taming Preference Mode Collapse via Directional Decoupling Alignment in Diffusion Reinforcement Learning
    "https://arxiv.org/abs/2512.24297",  # Figure It Out: Improve the Frontier of Reasoning with Executable Visual States
    "https://arxiv.org/abs/2512.24330",  # SenseNova-MARS: Empowering Multimodal Agentic Reasoning and Search via Reinforcement Learning
    "https://arxiv.org/abs/2512.24331",  # Spatial-aware Vision Language Model for Autonomous Driving
    "https://arxiv.org/abs/2512.24385",  # Forging Spatial Intelligence: A Roadmap of Multi-Modal Data Pre-Training for Autonomous Systems
    "https://arxiv.org/abs/2512.24426",  # Counterfactual VLA: Self-Reflective Vision-Language-Action Model with Adaptive Reasoning
    "https://arxiv.org/abs/2512.24497",  # What Drives Success in Physical Planning with Joint-Embedding Predictive World Models?
    "https://arxiv.org/abs/2512.24551",  # PhyGDPO: Physics-Aware Groupwise Direct Preference Optimization for Physically Consistent Text-to-Video Generation
    "https://arxiv.org/abs/2512.24601",  # Recursive Language Models
    "https://arxiv.org/abs/2512.24653",  # RoboMIND 2.0: A Multimodal, Bimanual Mobile Manipulation Dataset for Generalizable Embodied Intelligence
    "https://arxiv.org/abs/2512.24695",  # Nested Learning: The Illusion of Deep Learning Architectures
    "https://arxiv.org/abs/2512.24766",  # Dream2Flow: Bridging Video Generation and Open-World Manipulation with 3D Object Flow
    "https://arxiv.org/abs/2512.24880",  # mHC: Manifold-Constrained Hyper-Connections
    "https://arxiv.org/abs/2601.00092",  # Spatial4D-Bench: A Versatile 4D Spatial Intelligence Benchmark
    "https://arxiv.org/abs/2601.00116",  # GRL-SNAM: Geometric Reinforcement Learning with Path Differential Hamiltonians for Simultaneous Navigation and Mapping in Unknown Environments
    "https://arxiv.org/abs/2601.00215",  # From Sight to Insight: Improving Visual Reasoning Capabilities of Multimodal Models via Reinforcement Learning
    "https://arxiv.org/abs/2601.00504",  # MotionPhysics: Learnable Motion Distillation for Text-Guided Simulation
    "https://arxiv.org/abs/2601.00561",  # AEGIS: Exploring the Limit of World Knowledge Capabilities for Unified Mulitmodal Models
    "https://arxiv.org/abs/2601.00659",  # CRoPS: A Training-Free Hallucination Mitigation Framework for Vision-Language Models
    "https://arxiv.org/abs/2601.00844",  # Value-guided action planning with JEPA world models
    "https://arxiv.org/abs/2601.00898",  # Dichotomous Diffusion Policy Optimization
    "https://arxiv.org/abs/2601.00969",  # Value Vision-Language-Action Planning & Search
    "https://arxiv.org/abs/2601.01483",  # Unified Generation and Self-Verification for Vision-Language Models via Advantage Decoupled Preference Optimization
    "https://arxiv.org/abs/2601.01618",  # Action-Sketcher: From Reasoning to Action via Visual Sketches for Long-Horizon Robotic Manipulation
    "https://arxiv.org/abs/2601.01984",  # Thinking with Blueprints: Assisting Vision-Language Models in Spatial Reasoning via Structured Object Representation
    "https://arxiv.org/abs/2601.02036",  # GDRO: Group-level Reward Post-training Suitable for Diffusion Models
    "https://arxiv.org/abs/2601.02078",  # Genie Sim 3.0 : A High-Fidelity Comprehensive Simulation Platform for Humanoid Robot
    "https://arxiv.org/abs/2601.02256",  # VAR RL Done Right: Tackling Asynchronous Policy Conflicts in Visual Autoregressive Generation
    "https://arxiv.org/abs/2601.02295",  # CycleVLA: Proactive Self-Correcting Vision-Language-Action Models via Subtask Backtracking and Minimum Bayes Risk Decoding
    "https://arxiv.org/abs/2601.02356",  # Talk2Move: Reinforcement Learning for Text-Instructed Object-Level Geometric Transformation in Scenes
    "https://arxiv.org/abs/2601.02422",  # Watch Wider and Think Deeper: Collaborative Cross-modal Chain-of-Thought for Complex Visual Reasoning
    "https://arxiv.org/abs/2601.02427",  # NitroGen: An Open Foundation Model for Generalist Gaming Agents
    "https://arxiv.org/abs/2601.02456",  # InternVLA-A1: Unifying Understanding, Generation and Action for Robotic Manipulation
    "https://arxiv.org/abs/2601.02771",  # AbductiveMLLM: Boosting Visual Abductive Reasoning Within MLLMs
    "https://arxiv.org/abs/2601.02778",  # Closing the Reality Gap: Zero-Shot Sim-to-Real Deployment for Dexterous Force-Based Grasping and Manipulation
    "https://arxiv.org/abs/2601.02825",  # SketchThinker-R1: Towards Efficient Sketch-Style Reasoning in Large Multimodal Models
    "https://arxiv.org/abs/2601.03054",  # IBISAgent: Reinforcing Pixel-Level Visual Reasoning in MLLMs for Universal Biomedical Object Referring and Segmentation
    "https://arxiv.org/abs/2601.03192",  # MemRL: Self-Evolving Agents via Runtime Reinforcement Learning on Episodic Memory
    "https://arxiv.org/abs/2601.03193",  # UniCorn: Towards Self-Improving Unified Multimodal Models through Self-Generated Supervision
    "https://arxiv.org/abs/2601.03200",  # A High-Fidelity Digital Twin for Robotic Manipulation Based on 3D Gaussian Splatting
    "https://arxiv.org/abs/2601.03220",  # From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence
    "https://arxiv.org/abs/2601.03309",  # VLM4VLA: Revisiting Vision-Language-Models in Vision-Language-Action Models
    "https://arxiv.org/abs/2601.03665",  # PhysVideoGenerator: Towards Physically Aware Video Generation via Latent Physics Guidance
    "https://arxiv.org/abs/2601.03782",  # PointWorld: Scaling 3D World Models for In-The-Wild Robotic Manipulation
    "https://arxiv.org/abs/2601.03872",  # Atlas: Orchestrating Heterogeneous Models and Tools for Multi-Domain Complex Reasoning
    "https://arxiv.org/abs/2601.04033",  # Thinking with Frames: Generative Video Distortion Evaluation via Frame Reward Model
    "https://arxiv.org/abs/2601.04061",  # CLAP: Contrastive Latent Action Pretraining for Learning Vision-Language-Action Models from Human Videos
    "https://arxiv.org/abs/2601.04137",  # Wow, wo, val! A Comprehensive Embodied World Model Evaluation Turing Test
    "https://arxiv.org/abs/2601.04153",  # Diffusion-DRF: Free, Rich, and Differentiable Reward for Video Diffusion Fine-Tuning
    "https://arxiv.org/abs/2601.04441",  # Improving and Accelerating Offline RL in Large Discrete Action Spaces with Structured Policy Initialization
    "https://arxiv.org/abs/2601.04777",  # GeM-VG: Towards Generalized Multi-image Visual Grounding with Multimodal Large Language Models
    "https://arxiv.org/abs/2601.05172",  # CoV: Chain-of-View Prompting for Spatial Reasoning
    "https://arxiv.org/abs/2601.05230",  # Learning Latent Action World Models In The Wild
    "https://arxiv.org/abs/2601.05237",  # ObjectForesight: Predicting Future 3D Object Trajectories from Human Videos
    "https://arxiv.org/abs/2601.05242",  # GDPO: Group reward-Decoupled Normalization Policy Optimization for Multi-reward RL Optimization
    "https://arxiv.org/abs/2601.05244",  # GREx: Generalized Referring Expression Segmentation, Comprehension, and Generation
    "https://arxiv.org/abs/2601.05328",  # Bi-Orthogonal Factor Decomposition for Vision Transformers
    "https://arxiv.org/abs/2601.05344",  # Coding the Visual World: From Image to Simulation Using Vision Language Models
    "https://arxiv.org/abs/2601.05499",  # TOSC: Task-Oriented Shape Completion for Open-World Dexterous Grasp Generation from Partial Point Clouds
    "https://arxiv.org/abs/2601.05552",  # One Language-Free Foundation Model Is Enough for Universal Vision Anomaly Detection
    "https://arxiv.org/abs/2601.05600",  # SceneAlign: Aligning Multimodal Reasoning to Scene Graphs in Complex Visual Scenes
    "https://arxiv.org/abs/2601.05688",  # SketchVL: Policy Optimization via Fine-Grained Credit Assignment for Chart Understanding and More
    "https://arxiv.org/abs/2601.05848",  # Goal Force: Teaching Video Models To Accomplish Physics-Conditioned Goals
    "https://arxiv.org/abs/2601.05877",  # iReasoner: Trajectory-Aware Intrinsic Reasoning Supervision for Self-Evolving Large Multimodal Models
    "https://arxiv.org/abs/2601.06002",  # The Molecular Structure of Thought: Mapping the Topology of Long Chain-of-Thought Reasoning
    "https://arxiv.org/abs/2601.06521",  # BabyVision: Visual Reasoning Beyond Language
    "https://arxiv.org/abs/2601.06748",  # On-the-Fly VLA Adaptation via Test-Time Reinforcement Learning
    "https://arxiv.org/abs/2601.06794",  # No More Stale Feedback: Co-Evolving Critics for Open-World Agent Learning
    "https://arxiv.org/abs/2601.06803",  # Forest Before Trees: Latent Superposition for Efficient Visual Reasoning
    "https://arxiv.org/abs/2601.06993",  # Can Textual Reasoning Improve the Performance of MLLMs on Fine-grained Visual Classification?
    "https://arxiv.org/abs/2601.07055",  # Dr. Zero: Self-Evolving Search Agents without Training Data
    "https://arxiv.org/abs/2601.07060",  # PALM: Progress-Aware Policy Learning via Affordance Reasoning for Long-Horizon Robotic Manipulation
    "https://arxiv.org/abs/2601.07298",  # Mimic Human Cognition, Master Multi-Image Reasoning: A Meta-Action Framework for Enhanced Visual Understanding
    "https://arxiv.org/abs/2601.07645",  # PlaM: Training-Free Plateau-Guided Model Merging for Better Visual Grounding in MLLMs
    "https://arxiv.org/abs/2601.07701",  # Deep Whole-body Parkour
    "https://arxiv.org/abs/2601.07718",  # Hiking in the Wild: A Scalable Perceptive Parkour Framework for Humanoids
    "https://arxiv.org/abs/2601.07821",  # Failure-Aware RL: Reliable Offline-to-Online Reinforcement Learning with Self-Recovery for Real-World Manipulation
    "https://arxiv.org/abs/2601.07823",  # Video Generation Models in Robotics -- Applications, Research Challenges, Future Directions
    "https://arxiv.org/abs/2601.08325",  # ActiveVLA: Injecting Active Perception into Vision-Language-Action Models for Precise 3D Robotic Manipulation
    "https://arxiv.org/abs/2601.08499",  # EfficientFSL: Enhancing Few-Shot Classification via Query-Only Tuning in Vision Transformers
    "https://arxiv.org/abs/2601.08834",  # Reading or Reasoning? Format Decoupled Reinforcement Learning for Document OCR
    "https://arxiv.org/abs/2601.09295",  # MACRO-LLM: LLM-Empowered Multi-Agent Collaborative Reasoning under Spatiotemporal Partial Observability
    "https://arxiv.org/abs/2601.09430",  # Video-MSR: Benchmarking Multi-hop Spatial Reasoning Capabilities of MLLMs
    "https://arxiv.org/abs/2601.09512",  # CLARE: Continual Learning for Vision-Language-Action Models via Autonomous Adapter Routing and Expansion
    "https://arxiv.org/abs/2601.09518",  # Learning Whole-Body Human-Humanoid Interaction from Human-Human Demonstrations
    "https://arxiv.org/abs/2601.09536",  # Omni-R1: Towards the Unified Generative Paradigm for Multimodal Reasoning
    "https://arxiv.org/abs/2601.09667",  # Collaborative Multi-Agent Test-Time Reinforcement Learning for Reasoning
    "https://arxiv.org/abs/2601.09708",  # Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning
    "https://arxiv.org/abs/2601.09859",  # Breaking the Limits of Open-Weight CLIP: An Optimization Framework for Self-supervised Fine-tuning of CLIP
    "https://arxiv.org/abs/2601.10094",  # V-Zero: Self-Improving Multimodal Reasoning with Zero Annotation
    "https://arxiv.org/abs/2601.10129",  # LaViT: Aligning Latent Visual Thoughts for Multi-modal Reasoning
    "https://arxiv.org/abs/2601.10402",  # Toward Ultra-Long-Horizon Agentic Science: Cognitive Accumulation for Machine Learning Engineering
    "https://arxiv.org/abs/2601.10477",  # Urban Socio-Semantic Segmentation with Vision-Language Reasoning
    "https://arxiv.org/abs/2601.10497",  # MERGETUNE: Continued fine-tuning of vision-language models
    "https://arxiv.org/abs/2601.10553",  # Inference-time Physics Alignment of Video Generative Models with Latent World Models
    "https://arxiv.org/abs/2601.10679",  # Are Your Reasoning Models Reasoning or Guessing? A Mechanistic Analysis of Hierarchical Reasoning Models
    "https://arxiv.org/abs/2601.10744",  # Explore with Long-term Memory: A Benchmark and Multimodal LLM-based Reinforcement Learning Framework for Embodied Exploration
    "https://arxiv.org/abs/2601.10825",  # Reasoning Models Generate Societies of Thought
    "https://arxiv.org/abs/2601.10930",  # Where to Touch, How to Contact: Hierarchical RL-MPC Framework for Geometry-Aware Long-Horizon Dexterous Manipulation
    "https://arxiv.org/abs/2601.11087",  # PhysRVG: Physics-Aware Unified Reinforcement Learning for Video Generative Models
    "https://arxiv.org/abs/2601.11322",  # Enhancing Vision Language Models with Logic Reasoning for Situational Awareness
    "https://arxiv.org/abs/2601.11404",  # ACoT-VLA: Action Chain-of-Thought for Vision-Language-Action Models
    "https://arxiv.org/abs/2601.11421",  # The Great March 100: 100 Detail-oriented Tasks for Evaluating Embodied AI Agents
    "https://arxiv.org/abs/2601.11442",  # Map2Thought: Explicit 3D Spatial Reasoning via Metric Cognitive Maps
    "https://arxiv.org/abs/2601.11729",  # SpaRRTa: A Synthetic Benchmark for Evaluating Spatial Intelligence in Visual Foundation Models
    "https://arxiv.org/abs/2601.12538",  # Agentic Reasoning for Large Language Models
    "https://arxiv.org/abs/2601.12585",  # Do MLLMs See What We See? Analyzing Visualization Literacy Barriers in AI Systems
    "https://arxiv.org/abs/2601.12796",  # Contact-Aware Neural Dynamics
    "https://arxiv.org/abs/2601.12964",  # Cross-Scale Pretraining: Enhancing Self-Supervised Learning for Low-Resolution Satellite Imagery for Semantic Segmentation
    "https://arxiv.org/abs/2601.13132",  # GaussExplorer: 3D Gaussian Splatting for Embodied Exploration and Reasoning
    "https://arxiv.org/abs/2601.13304",  # CausalSpatial: A Benchmark for Object-Centric Causal Spatial Reasoning
    "https://arxiv.org/abs/2601.13562",  # Reasoning is a Modality
    "https://arxiv.org/abs/2601.13633",  # Scaling Test-time Inference for Visual Grounding
    "https://arxiv.org/abs/2601.13705",  # Reasoning or Pattern Matching? Probing Large Vision-Language Models with Visual Puzzles
    "https://arxiv.org/abs/2601.13942",  # Glance-or-Gaze: Incentivizing LMMs to Adaptively Focus Search via Reinforcement Learning
    "https://arxiv.org/abs/2601.14127",  # The Side Effects of Being Smart: Safety Risks in MLLMs' Multi-Image Reasoning
    "https://arxiv.org/abs/2601.14209",  # InT: Self-Proposed Interventions Enable Credit Assignment in LLM Reasoning
    "https://arxiv.org/abs/2601.14234",  # Q-learning with Adjoint Matching
    "https://arxiv.org/abs/2601.14339",  # CityCube: Benchmarking Cross-view Spatial Reasoning on Vision-Language Models in Urban Environments
    "https://arxiv.org/abs/2601.14352",  # RoboBrain 2.5: Depth in Sight, Time in Mind
    "https://arxiv.org/abs/2601.14354",  # VJEPA: Variational Joint Embedding Predictive Architectures as Probabilistic World Models
    "https://arxiv.org/abs/2601.14514",  # "Just in Time" World Modeling Supports Human Planning and Reasoning
    "https://arxiv.org/abs/2601.15164",  # V-CAGE: Context-Aware Generation and Verification for Scalable Long-Horizon Embodied Tasks
    "https://arxiv.org/abs/2601.15224",  # PROGRESSLM: Towards Progress Reasoning in Vision-Language Models
    "https://arxiv.org/abs/2601.15275",  # RayRoPE: Projective Ray Positional Encoding for Multi-view Attention
    "https://arxiv.org/abs/2601.15282",  # Rethinking Video Generation Model for the Embodied World
    "https://arxiv.org/abs/2601.15419",  # Learning a Unified Latent Space for Cross-Embodiment Robot Control
    "https://arxiv.org/abs/2601.15533",  # From Generative Engines to Actionable Simulators: The Imperative of Physical Grounding in World Models
    "https://arxiv.org/abs/2601.15715",  # RebuttalAgent: Strategic Persuasion in Academic Rebuttal via Theory of Mind
    "https://arxiv.org/abs/2601.16093",  # SAMTok: Representing Any Mask with Two Words
    "https://arxiv.org/abs/2601.16148",  # ActionMesh: Animated 3D Mesh Generation with Temporal 3D Diffusion
    "https://arxiv.org/abs/2601.16163",  # Cosmos Policy: Fine-Tuning Video Models for Visuomotor Control and Planning
    "https://arxiv.org/abs/2601.16175",  # Learning to Discover at Test Time
    "https://arxiv.org/abs/2601.16212",  # Point Bridge: 3D Representations for Cross Domain Policy Learning
    "https://arxiv.org/abs/2601.16520",  # TangramPuzzle: Evaluating Multimodal Large Language Models with Compositional Spatial Reasoning
    "https://arxiv.org/abs/2601.16538",  # OnlineSI: Taming Large Language Model for Online 3D Understanding and Grounding
    "https://arxiv.org/abs/2601.16973",  # VisGym: Diverse, Customizable, Scalable Environments for Multimodal Agents
    "https://arxiv.org/abs/2601.17067",  # A Mechanistic View on Video Generation as World Models: State and Dynamics
    "https://arxiv.org/abs/2601.17251",  # EMPM: Embodied MPM for Modeling and Simulation of Deformable Objects
    "https://arxiv.org/abs/2601.17440",  # PILOT: A Perceptive Integrated Low-level Controller for Loco-manipulation over Unstructured Scenes
    "https://arxiv.org/abs/2601.17486",  # EquiForm: Noise-Robust SE(3)-Equivariant Policy Learning from 3D Point Clouds
    "https://arxiv.org/abs/2601.17616",  # Split-on-Share: Mixture of Sparse Experts for Task-Agnostic Continual Learning
    "https://arxiv.org/abs/2601.17868",  # VidLaDA: Bidirectional Diffusion Large Language Models for Efficient Video Understanding
    "https://arxiv.org/abs/2601.18067",  # EvolVE: Evolutionary Search for LLM-based Verilog Generation and Optimization
    "https://arxiv.org/abs/2601.18323",  # TC-IDM: Grounding Video Generation for Executable Zero-shot Robot Motion
    "https://arxiv.org/abs/2601.18340",  # Beyond Rigid: Benchmarking Non-Rigid Video Editing
    "https://arxiv.org/abs/2601.18533",  # From Verifiable Dot to Reward Chain: Harnessing Verifiable Reference-based Rewards for Reinforcement Learning of Open-ended Generation
    "https://arxiv.org/abs/2601.18577",  # Self-Refining Video Sampling
    "https://arxiv.org/abs/2601.18631",  # AdaReasoner: Dynamic Tool Orchestration for Iterative Visual Reasoning
    "https://arxiv.org/abs/2601.18692",  # A Pragmatic VLA Foundation Model
    "https://arxiv.org/abs/2601.18734",  # Self-Distilled Reasoner: On-Policy Self-Distillation for Large Language Models
    "https://arxiv.org/abs/2601.18795",  # Reuse your FLOPs: Scaling RL on Hard Problems by Conditioning on Very Off-Policy Prefixes
    "https://arxiv.org/abs/2601.19030",  # A Unifying View of Coverage in Linear Off-Policy Evaluation
    "https://arxiv.org/abs/2601.19099",  # m2sv: A Scalable Benchmark for Map-to-Street-View Spatial Reasoning
    "https://arxiv.org/abs/2601.19204",  # MATA: A Trainable Hierarchical Automaton System for Multi-Agent Visual Reasoning
    "https://arxiv.org/abs/2601.19280",  # Group Distributionally Robust Optimization-Driven Reinforcement Learning for LLM Reasoning
    "https://arxiv.org/abs/2601.19336",  # From Observations to Events: Event-Aware World Model for Reinforcement Learning
    "https://arxiv.org/abs/2601.19439",  # OSIRIS: Bridging Analog Circuit Design and Machine Learning with Scalable Dataset Generation
    "https://arxiv.org/abs/2601.19452",  # APC-RL: Exceeding Data-Driven Behavior Priors with Adaptive Policy Composition
    "https://arxiv.org/abs/2601.19612",  # Safe Exploration via Policy Priors
    "https://arxiv.org/abs/2601.19686",  # Video-KTR: Reinforcing Video Reasoning via Key Token Attribution
    "https://arxiv.org/abs/2601.19707",  # Scalable Exploration for High-Dimensional Continuous Control via Value-Guided Flow
    "https://arxiv.org/abs/2601.19810",  # Unsupervised Learning of Efficient Exploration: Pre-training Adaptive Policies via Self-Imposed Goals
    "https://arxiv.org/abs/2601.19834",  # Visual Generation Unlocks Human-Like Reasoning through Multimodal World Models
    "https://arxiv.org/abs/2601.19897",  # Self-Distillation Enables Continual Learning
    "https://arxiv.org/abs/2601.20071",  # Distributional value gradients for stochastic environments
    "https://arxiv.org/abs/2601.20218",  # DenseGRPO: From Sparse to Dense Reward for Flow Matching Model Alignment
    "https://arxiv.org/abs/2601.20321",  # TaF-VLA: Tactile-Force Alignment in Vision-Language-Action Models for Force-aware Manipulation
    "https://arxiv.org/abs/2601.20354",  # Everything in Its Place: Benchmarking Spatial Intelligence of Text-to-Image Models
    "https://arxiv.org/abs/2601.20540",  # Advancing Open-source World Models
    "https://arxiv.org/abs/2601.20614",  # Harder Is Better: Boosting Mathematical Reasoning via Difficulty-Aware GRPO and Multi-Aspect Question Reformulation
    "https://arxiv.org/abs/2601.20765",  # Less is More: Clustered Cross-Covariance Control for Offline RL
    "https://arxiv.org/abs/2601.20802",  # Reinforcement Learning via Self-Distillation
    "https://arxiv.org/abs/2601.21037",  # Thinking in Frames: How Visual Context and Test-Time Scaling Empower Video Reasoning
    "https://arxiv.org/abs/2601.21187",  # FRISM: Fine-Grained Reasoning Injection via Subspace-Level Model Merging for Vision-Language Models
    "https://arxiv.org/abs/2601.21199",  # Thinker: A vision-language foundation model for embodied intelligence
    "https://arxiv.org/abs/2601.21282",  # WorldBench: Disambiguating Physics for Diagnostic Evaluation of World Models
    "https://arxiv.org/abs/2601.21343",  # Self-Improving Pretraining: using post-trained models to pretrain better models
    "https://arxiv.org/abs/2601.21363",  # Towards Bridging the Gap between Large-Scale Pretraining and Efficient Finetuning for Humanoid Control
    "https://arxiv.org/abs/2601.21598",  # Beyond Imitation: Reinforcement Learning for Active Latent Planning
    "https://arxiv.org/abs/2601.21634",  # RSGround-R1: Rethinking Remote Sensing Visual Grounding through Spatial Reasoning
    "https://arxiv.org/abs/2601.21725",  # Procedural Pretraining: Warming Up Language Models with Abstract Data
    "https://arxiv.org/abs/2601.21845",  # Constrained Meta Reinforcement Learning with Provable Test-Time Safety
    "https://arxiv.org/abs/2601.21872",  # WebArbiter: A Principle-Guided Reasoning Process Reward Model for Web Agents
    "https://arxiv.org/abs/2601.21969",  # Token-Guard: Towards Token-Level Hallucination Control via Self-Checking Decoding
    "https://arxiv.org/abs/2601.21998",  # Causal World Modeling for Robot Control
    "https://arxiv.org/abs/2601.22135",  # PI-Light: Physics-Inspired Diffusion for Full-Image Relighting
    "https://arxiv.org/abs/2601.22153",  # DynamicVLA: A Vision-Language-Action Model for Dynamic Object Manipulation
    "https://arxiv.org/abs/2601.22231",  # Geometry without Position? When Positional Embeddings Help and Hurt Spatial Reasoning
    "https://arxiv.org/abs/2601.22550",  # Exo-Plore: Exploring Exoskeleton Control Space through Human-aligned Simulation
    "https://arxiv.org/abs/2601.22595",  # Learn More with Less: Uncertainty Consistency Guided Query Selection for RLVR
    "https://arxiv.org/abs/2601.22628",  # TTCS: Test-Time Curriculum Synthesis for Self-Evolving
    "https://arxiv.org/abs/2601.23265",  # PaperBanana: Automating Academic Illustration for AI Scientists
    "https://arxiv.org/abs/2602.00170",  # The Blessing of Dimensionality in LLM Fine-tuning: A Variance-Curvature Perspective
    "https://arxiv.org/abs/2602.00359",  # Position: Agentic Evolution is the Path to Evolving LLMs
    "https://arxiv.org/abs/2602.00462",  # LatentLens: Revealing Highly Interpretable Visual Tokens in LLMs
    "https://arxiv.org/abs/2602.00475",  # Parallel Stochastic Gradient-Based Planning for World Models
    "https://arxiv.org/abs/2602.00528",  # How Far Are LLMs from Professional Poker Players? Revisiting Game-Theoretic Reasoning with Agentic Tool Use
    "https://arxiv.org/abs/2602.00551",  # APEX: A Decoupled Memory-based Explorer for Asynchronous Aerial Object Goal Navigation
    "https://arxiv.org/abs/2602.00574",  # Learning Modal-Mixed Chain-of-Thought Reasoning with Latent Embeddings
    "https://arxiv.org/abs/2602.00629",  # Action-Free Offline-to-Online RL via Discretised State Policies
    "https://arxiv.org/abs/2602.00678",  # Toward Reliable Sim-to-Real Predictability for MoE-based Robust Quadrupedal Locomotion
    "https://arxiv.org/abs/2602.00743",  # SA-VLA: Spatially-Aware Flow-Matching for Vision-Language-Action Reinforcement Learning
    "https://arxiv.org/abs/2602.00795",  # DVLA-RL: Dual-Level Vision-Language Alignment with Reinforcement Learning Gating for Few-Shot Learning
    "https://arxiv.org/abs/2602.00915",  # UniMorphGrasp: Diffusion Model with Morphology-Awareness for Cross-Embodiment Dexterous Grasp Generation
    "https://arxiv.org/abs/2602.00937",  # CLAMP: Contrastive Learning for 3D Multi-View Action-Conditioned Robotic Manipulation Pretraining
    "https://arxiv.org/abs/2602.00971",  # Unveiling the Cognitive Compass: Theory-of-Mind-Guided Multimodal Emotion Reasoning
    "https://arxiv.org/abs/2602.01058",  # Good SFT Optimizes for SFT, Better SFT Prepares for Reinforcement Learning
    "https://arxiv.org/abs/2602.01153",  # UniForce: A Unified Latent Force Model for Robot Manipulation with Diverse Tactile Sensors
    "https://arxiv.org/abs/2602.01156",  # PolicyFlow: Policy Optimization with Continuous Normalizing Flow in Reinforcement Learning
    "https://arxiv.org/abs/2602.01166",  # Latent Reasoning VLA: Latent Thinking and Prediction for Vision-Language-Action Models
    "https://arxiv.org/abs/2602.01270",  # Mixture-of-World Models: Scaling Multi-Task Reinforcement Learning with Modular Latent Dynamics
    "https://arxiv.org/abs/2602.01515",  # RAPT: Model-Predictive Out-of-Distribution Detection and Failure Diagnosis for Sim-to-Real Humanoid Robots
    "https://arxiv.org/abs/2602.01601",  # Adaptive Rollout Allocation for Online Reinforcement Learning with Verifiable Rewards
    "https://arxiv.org/abs/2602.01619",  # SUSD: Structured Unsupervised Skill Discovery through State Factorization
    "https://arxiv.org/abs/2602.01630",  # Research on World Models Is Not Merely Injecting World Knowledge into Specific Tasks
    "https://arxiv.org/abs/2602.01640",  # A2Eval: Agentic and Automated Evaluation for Embodied Brain
    "https://arxiv.org/abs/2602.01685",  # Semantic-aware Wasserstein Policy Regularization for Large Language Model Alignment
    "https://arxiv.org/abs/2602.01789",  # RFS: Reinforcement Learning with Residual Flow Steering for Dexterous Manipulation
    "https://arxiv.org/abs/2602.01811",  # From Knowing to Doing Precisely: A General Self-Correction and Termination Framework for VLA models
    "https://arxiv.org/abs/2602.01816",  # Seeing Is Believing? A Benchmark for Multimodal Large Language Models on Visual Illusions and Anomalies
    "https://arxiv.org/abs/2602.01905",  # Learning Sparse Visual Representations via Spatial-Semantic Factorization
    "https://arxiv.org/abs/2602.01939",  # Towards Exploratory and Focused Manipulation with Bimanual Active Perception: A New Problem, Benchmark and Strategy
    "https://arxiv.org/abs/2602.01960",  # Grounding Generated Videos in Feasible Plans via World Models
    "https://arxiv.org/abs/2602.01962",  # Zero-Shot Off-Policy Learning
    "https://arxiv.org/abs/2602.01984",  # Enhancing Multi-Image Understanding through Delimiter Token Scaling
    "https://arxiv.org/abs/2602.02004",  # ClueTracer: Question-to-Vision Clue Tracing for Training-Free Hallucination Suppression in Multimodal Reasoning
    "https://arxiv.org/abs/2602.02140",  # Quantifying the Gap between Understanding and Generation within Unified Multimodal Models
    "https://arxiv.org/abs/2602.02142",  # FD-VLA: Force-Distilled Vision-Language-Action Model for Contact-Rich Manipulation
    "https://arxiv.org/abs/2602.02150",  # ECHO: Entropy-Confidence Hybrid Optimization for Test-Time Reinforcement Learning
    "https://arxiv.org/abs/2602.02156",  # LoopViT: Scaling Visual ARC with Looped Transformers
    "https://arxiv.org/abs/2602.02196",  # TIDE: Trajectory-based Diagnostic Evaluation of Test-Time Improvement in LLM Agents
    "https://arxiv.org/abs/2602.02381",  # Self-Supervised Learning from Structural Invariance
    "https://arxiv.org/abs/2602.02402",  # SoMA: A Real-to-Sim Neural Simulator for Robotic Soft-body Manipulation
    "https://arxiv.org/abs/2602.02453",  # Thinking with Comics: Enhancing Multimodal Reasoning through Structured Visual Storytelling
    "https://arxiv.org/abs/2602.02454",  # World-Gymnast: Training Robots with Reinforcement Learning in a World Model
    "https://arxiv.org/abs/2602.02465",  # MentisOculi: Revealing the Limits of Reasoning with Mental Imagery
    "https://arxiv.org/abs/2602.02473",  # HumanX: Toward Agile and Generalizable Humanoid Interaction Skills from Human Videos
    "https://arxiv.org/abs/2602.02481",  # Flow Policy Gradients for Robot Control
    "https://arxiv.org/abs/2602.02488",  # RLAnything: Forge Environment, Policy, and Reward Model in Completely Dynamic RL System
    "https://arxiv.org/abs/2602.02605",  # Fine-Tuning Language Models to Know What They Know
    "https://arxiv.org/abs/2602.02710",  # Maximum Likelihood Reinforcement Learning
    "https://arxiv.org/abs/2602.02722",  # Hierarchical Entity-centric Reinforcement Learning with Factored Subgoal Diffusion
    "https://arxiv.org/abs/2602.02762",  # On the Sample Efficiency of Inverse Dynamics Models for Semi-Supervised Imitation Learning
    "https://arxiv.org/abs/2602.02951",  # Nüwa: Mending the Spatial Integrity Torn by VLM Token Pruning
    "https://arxiv.org/abs/2602.02960",  # Embodiment-Aware Generalist Specialist Distillation for Unified Humanoid Whole-Body Control
    "https://arxiv.org/abs/2602.03002",  # RPL: Learning Robust Humanoid Perceptive Locomotion on Challenging Terrains
    "https://arxiv.org/abs/2602.03086",  # Neural Predictor-Corrector: Solving Homotopy Problems with Reinforcement Learning
    "https://arxiv.org/abs/2602.03120",  # Quantized Evolution Strategies: High-precision Fine-tuning of Quantized LLMs at Low-precision Cost
    "https://arxiv.org/abs/2602.03143",  # Self-Hinting Language Models Enhance Reinforcement Learning
    "https://arxiv.org/abs/2602.03361",  # Z3D: Zero-Shot 3D Visual Grounding from Images
    "https://arxiv.org/abs/2602.03445",  # CRL-VLA: Continual Vision-Language-Action Learning
    "https://arxiv.org/abs/2602.03627",  # Ultra Fast PDE Solving via Physics Guided Few-step Diffusion
    "https://arxiv.org/abs/2602.03733",  # RegionReasoner: Region-Grounded Multi-Round Visual Reasoning
    "https://arxiv.org/abs/2602.03782",  # QVLA: Not All Channels Are Equal in Vision-Language-Action Model's Quantization
    "https://arxiv.org/abs/2602.03783",  # Efficient Estimation of Kernel Surrogate Models for Task Attribution
    "https://arxiv.org/abs/2602.03806",  # Bridging Online and Offline RL: Contextual Bandit Learning for Multi-Turn Code Generation
    "https://arxiv.org/abs/2602.03916",  # SpatiaLab: Can Vision-Language Models Perform Spatial Reasoning in the Wild?
    "https://arxiv.org/abs/2602.03973",  # VLS: Steering Pretrained Robot Policies via Vision-Language Models
    "https://arxiv.org/abs/2602.04118",  # Learning to Reason in 13 Parameters
    "https://arxiv.org/abs/2602.04145",  # Training Data Efficiency in Multimodal Process Reward Models
    "https://arxiv.org/abs/2602.04411",  # Self-evolving Embodied AI
    "https://arxiv.org/abs/2602.04413",  # History-Guided Iterative Visual Reasoning with Self-Correction
    "https://arxiv.org/abs/2602.04600",  # Act, Sense, Act: Learning Non-Markovian Active Perception Strategies from Large-Scale Egocentric Human Data
    "https://arxiv.org/abs/2602.04755",  # When Silence Is Golden: Can LLMs Learn to Abstain in Temporal QA and Beyond?
    "https://arxiv.org/abs/2602.04837",  # Group-Evolving Agents: Open-Ended Self-Improvement via Experience Sharing
    "https://arxiv.org/abs/2602.04879",  # Rethinking the Trust Region in LLM Reinforcement Learning
    "https://arxiv.org/abs/2602.04884",  # Reinforced Attention Learning
    "https://arxiv.org/abs/2602.05051",  # ReFORM: Reflected Flows for On-support Offline RL via Noise Manipulation
    "https://arxiv.org/abs/2602.05089",  # Beware Untrusted Simulators -- Reward-Free Backdoor Attacks in Reinforcement Learning
    "https://arxiv.org/abs/2602.05179",  # From Sequential to Parallel: Reformulating Dynamic Programming as GPU Kernels for Large-Scale Stochastic Combinatorial Optimization
    "https://arxiv.org/abs/2602.05323",  # GAS: Enhancing Reward-Cost Balance of Generative Model-assisted Offline Safe RL
    "https://arxiv.org/abs/2602.05359",  # Multimodal Latent Reasoning via Hierarchical Visual Cues Injection
    "https://arxiv.org/abs/2602.05449",  # DisCa: Accelerating Video Diffusion Transformers with Distillation-Compatible Learnable Feature Caching
    "https://arxiv.org/abs/2602.05468",  # TaSA: Two-Phased Deep Predictive Learning of Tactile Sensory Attenuation for Improving In-Grasp Manipulation
    "https://arxiv.org/abs/2602.05547",  # Multi-Task GRPO: Reliable LLM Reasoning Across Tasks
    "https://arxiv.org/abs/2602.05755",  # FMPose3D: monocular 3D pose estimation via flow matching
    "https://arxiv.org/abs/2602.05791",  # Scalable and General Whole-Body Control for Cross-Humanoid Locomotion
    "https://arxiv.org/abs/2602.05842",  # Reinforcement World Model Learning for LLM-based Agents
    "https://arxiv.org/abs/2602.05943",  # Orthogonal Model Merging
    "https://arxiv.org/abs/2602.05986",  # RISE-Video: Can Video Generators Decode Implicit World Rules?
    "https://arxiv.org/abs/2602.06001",  # Visuo-Tactile World Models
    "https://arxiv.org/abs/2602.06033",  # Can vision language models learn intuitive physics from interaction?
    "https://arxiv.org/abs/2602.06035",  # InterPrior: Scaling Generative Control for Physics-Based Human-Object Interactions
    "https://arxiv.org/abs/2602.06037",  # Thinking with Geometry: Active Geometry Integration for Spatial Reasoning
    "https://arxiv.org/abs/2602.06043",  # Shared LoRA Subspaces for almost Strict Continual Learning
    "https://arxiv.org/abs/2602.06130",  # Self-Improving World Modelling with Latent Actions
    "https://arxiv.org/abs/2602.06218",  # Cross-Modal Redundancy and the Geometry of Vision-Language Embeddings
    "https://arxiv.org/abs/2602.06341",  # HiWET: Hierarchical World-Frame End-Effector Tracking for Long-Horizon Humanoid Loco-Manipulation
    "https://arxiv.org/abs/2602.06445",  # ECO: Energy-Constrained Optimization with Reinforcement Learning for Humanoid Walking
    "https://arxiv.org/abs/2602.06508",  # World-VLA-Loop: Closed-Loop Learning of Video World Model and VLA Policy
    "https://arxiv.org/abs/2602.06556",  # LIBERO-X: Robustness Litmus for Vision-Language-Action Models
    "https://arxiv.org/abs/2602.06572",  # The Law of Task-Achieving Body Motion: Axiomatizing Success of Robot Manipulation Actions
    "https://arxiv.org/abs/2602.06643",  # Humanoid Manipulation Interface: Humanoid Whole-Body Manipulation from Robot-Free Demonstrations
    "https://arxiv.org/abs/2602.06827",  # DynaRetarget: Dynamically-Feasible Retargeting using Sampling-Based Trajectory Optimization
    "https://arxiv.org/abs/2602.06854",  # SEMA: Simple yet Effective Learning for Multi-Turn Jailbreak Attacks
    "https://arxiv.org/abs/2602.06949",  # DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos
    "https://arxiv.org/abs/2602.07050",  # Interpreting Physics in Video World Models
    "https://arxiv.org/abs/2602.07227",  # Cerebellar-Inspired Residual Control for Fault Recovery: From Inference-Time Adaptation to Structural Consolidation
    "https://arxiv.org/abs/2602.07322",  # Action-to-Action Flow Matching
    "https://arxiv.org/abs/2602.07326",  # Why Look at It at All?: Vision-Free Multifingered Blind Grasping Using Uniaxial Fingertip Force Sensing
    "https://arxiv.org/abs/2602.07588",  # Unified Biomolecular Trajectory Generation via Pretrained Variational Bridge
    "https://arxiv.org/abs/2602.07605",  # Fine-R1: Make Multi-modal LLMs Excel in Fine-Grained Visual Recognition by Chain-of-Thought Reasoning
    "https://arxiv.org/abs/2602.07845",  # Recurrent-Depth VLA: Implicit Test-Time Compute Scaling of Vision-Language-Action Models via Latent Iterative Reasoning
    "https://arxiv.org/abs/2602.07854",  # Geometry-Aware Rotary Position Embedding for Consistent Video World Model
    "https://arxiv.org/abs/2602.08025",  # MIND: Benchmarking Memory Consistency and Action Control in World Models
    "https://arxiv.org/abs/2602.08032",  # Horizon Imagination: Efficient On-Policy Rollout in Diffusion World Models
    "https://arxiv.org/abs/2602.08040",  # FIRE: Frobenius-Isometry Reinitialization for Balancing the Stability-Plasticity Tradeoff
    "https://arxiv.org/abs/2602.08145",  # Reliable and Responsible Foundation Models: A Comprehensive Survey
    "https://arxiv.org/abs/2602.08234",  # SkillRL: Evolving Agents via Recursive Skill-Augmented Reinforcement Learning
    "https://arxiv.org/abs/2602.08236",  # When and How Much to Imagine: Adaptive Test-Time Scaling with World Models for Visual Spatial Reasoning
    "https://arxiv.org/abs/2602.08241",  # Do MLLMs Really See It: Reinforcing Visual Attention in Multimodal LLMs
    "https://arxiv.org/abs/2602.08278",  # DexFormer: Cross-Embodied Dexterous Manipulation via History-Conditioned Transformer
    "https://arxiv.org/abs/2602.08346",  # What, Whether and How? Unveiling Process Reward Models for Thinking with Images Reasoning
    "https://arxiv.org/abs/2602.08683",  # OneVision-Encoder: Codec-Aligned Sparsity as a Foundational Principle for Multimodal Intelligence
    "https://arxiv.org/abs/2602.08971",  # WorldArena: A Unified Benchmark for Evaluating Perception and Functional Utility of Embodied World Models
    "https://arxiv.org/abs/2602.09013",  # Dexterous Manipulation Policies from RGB Human Videos via 3D Hand-Object Trajectory Reconstruction
    "https://arxiv.org/abs/2602.09022",  # WorldCompass: Reinforcement Learning for Long-Horizon World Models
    "https://arxiv.org/abs/2602.09276",  # Effective Reasoning Chains Reduce Intrinsic Dimensionality
    "https://arxiv.org/abs/2602.09463",  # SpotAgent: Grounding Visual Geo-localization in Large Vision-Language Models through Agentic Reasoning
    "https://arxiv.org/abs/2602.09617",  # AnyTouch 2: General Optical Tactile Representation Learning For Dynamic Tactile Perception
    "https://arxiv.org/abs/2602.09657",  # AutoFly: Vision-Language-Action Model for UAV Autonomous Navigation in the Wild
    "https://arxiv.org/abs/2602.09878",  # MVISTA-4D: View-Consistent 4D World Model with Test-Time Action Inference for Robotic Manipulation
    "https://arxiv.org/abs/2602.09973",  # RoboInter: A Holistic Intermediate Representation Suite Towards Robotic Manipulation
    "https://arxiv.org/abs/2602.10013",  # Learning Force-Regulated Manipulation with a Low-Cost Tactile-Force-Controlled Gripper
    "https://arxiv.org/abs/2602.10094",  # 4RC: 4D Reconstruction via Conditional Querying Anytime and Anywhere
    "https://arxiv.org/abs/2602.10098",  # VLA-JEPA: Enhancing Vision-Language-Action Model with Latent World Model
    "https://arxiv.org/abs/2602.10102",  # VideoWorld 2: Learning Transferable Knowledge from Real-world Videos
    "https://arxiv.org/abs/2602.10106",  # EgoHumanoid: Unlocking In-the-Wild Loco-Manipulation with Robot-Free Egocentric Demonstration
    "https://arxiv.org/abs/2602.10109",  # ST4VLA: Spatially Guided Training for Vision-Language-Action Models
    "https://arxiv.org/abs/2602.10116",  # SAGE: Scalable Agentic 3D Scene Generation for Embodied AI
    "https://arxiv.org/abs/2602.10503",  # Towards Long-Lived Robots: Continual Learning VLA Models via Reinforcement Fine-Tuning
    "https://arxiv.org/abs/2602.10520",  # Prioritize the Process, Not Just the Outcome: Rewarding Latent Thought Trajectories Improves Reasoning in Looped Language Models
    "https://arxiv.org/abs/2602.10551",  # C^2ROPE: Causal Continuous Rotary Positional Encoding for 3D Large Multimodal-Models Reasoning
    "https://arxiv.org/abs/2602.10556",  # LAP: Language-Action Pre-Training Enables Zero-shot Cross-Embodiment Transfer
    "https://arxiv.org/abs/2602.10675",  # TwiFF (Think With Future Frames): A Large-Scale Dataset for Dynamic Visual Reasoning
    "https://arxiv.org/abs/2602.10698",  # AugVLA-3D: Depth-Driven Feature Augmentation for Vision-Language-Action Models
    "https://arxiv.org/abs/2602.10717",  # Say, Dream, and Act: Learning Video World Models for Instruction-Driven Robot Manipulation
    "https://arxiv.org/abs/2602.10815",  # Why Does RL Generalize Better Than SFT? A Data-Centric Perspective on VLM Post-Training
    "https://arxiv.org/abs/2602.11057",  # Divide, Harmonize, Then Conquer It: Shooting Multi-Commodity Flow Problems with Multimodal Language Models
    "https://arxiv.org/abs/2602.11073",  # Chatting with Images for Introspective Visual Thinking
    "https://arxiv.org/abs/2602.11075",  # RISE: Self-Improving Robot Policy with Compositional World Model
    "https://arxiv.org/abs/2602.11124",  # PhyCritic: Multimodal Critic Models for Physical AI
    "https://arxiv.org/abs/2602.11144",  # GENIUS: Generative Fluid Intelligence Evaluation Suite
    "https://arxiv.org/abs/2602.11217",  # The Magic Correlations: Understanding Knowledge Transfer from Pretraining to Supervised Fine-Tuning
    "https://arxiv.org/abs/2602.11236",  # ABot-M0: VLA Foundation Model for Robotic Manipulation with Action Manifold Learning
    "https://arxiv.org/abs/2602.11241",  # Active Zero: Self-Evolving Vision-Language Models through Active Environment Exploration
    "https://arxiv.org/abs/2602.11291",  # H-WM: Robotic Task and Motion Planning Guided by Hierarchical World Model
    "https://arxiv.org/abs/2602.11337",  # MolmoSpaces: A Large-Scale Open Ecosystem for Robot Navigation and Manipulation
    "https://arxiv.org/abs/2602.11389",  # Causal-JEPA: Learning World Models through Object-Level Latent Interventions
    "https://arxiv.org/abs/2602.11393",  # Human Preference Modeling Using Visual Motion Prediction Improves Robot Skill Learning from Egocentric Human Video
    "https://arxiv.org/abs/2602.11437",  # Distributionally Robust Cooperative Multi-Agent Reinforcement Learning via Robust Value Factorization
    "https://arxiv.org/abs/2602.11523",  # Unifying Stable Optimization and Reference Regularization in RLHF
    "https://arxiv.org/abs/2602.11549",  # Native Reasoning Models: Training Language Models to Reason on Unverifiable Data
    "https://arxiv.org/abs/2602.11635",  # Do MLLMs Really Understand Space? A Mathematical Reasoning Evaluation
    "https://arxiv.org/abs/2602.11730",  # STVG-R1: Incentivizing Instance-Level Reasoning and Grounding in Videos via Reinforcement Learning
    "https://arxiv.org/abs/2602.11737",  # Mask What Matters: Mitigating Object Hallucinations in Multimodal Large Language Models with Object-Aligned Visual Contrastive Decoding
    "https://arxiv.org/abs/2602.11779",  # Temperature as a Meta-Policy: Adaptive Temperature in LLM Reinforcement Learning
    "https://arxiv.org/abs/2602.11812",  # Predicting LLM Output Length via Entropy-Guided Representations
    "https://arxiv.org/abs/2602.11832",  # JEPA-VLA: Video Predictive Embedding is Needed for VLA Models
    "https://arxiv.org/abs/2602.11858",  # Zooming without Zooming: Region-to-Image Distillation for Fine-Grained Multimodal Perception
    "https://arxiv.org/abs/2602.11964",  # Gaia2: Benchmarking LLM Agents on Dynamic and Asynchronous Environments
    "https://arxiv.org/abs/2602.12032",  # When would Vision-Proprioception Policies Fail in Robotic Manipulation?
    "https://arxiv.org/abs/2602.12062",  # HoloBrain-0 Technical Report
    "https://arxiv.org/abs/2602.12063",  # VLAW: Iterative Co-Improvement of Vision-Language-Action Policy and World Model
    "https://arxiv.org/abs/2602.12087",  # Geometry of Uncertainty: Learning Metric Spaces for Multimodal State Estimation in RL
    "https://arxiv.org/abs/2602.12099",  # GigaBrain-0.5M*: a VLA That Learns From World Model-Based Reinforcement Learning
    "https://arxiv.org/abs/2602.12113",  # Stop Unnecessary Reflection: Training LRMs for Efficient Reasoning with Adaptive Reflection and Length Coordinated Penalty
    "https://arxiv.org/abs/2602.12116",  # P-GenRM: Personalized Generative Reward Model with Test-time User-based Scaling
    "https://arxiv.org/abs/2602.12159",  # 3DGSNav: Enhancing Vision-Language Model Reasoning for Object Navigation via Active 3D Gaussian Splatting
    "https://arxiv.org/abs/2602.12205",  # DeepGen 1.0: A Lightweight Unified Multimodal Model for Advancing Image Generation and Editing
    "https://arxiv.org/abs/2602.12215",  # LDA-1B: Scaling Latent Dynamics Action Model via Universal Embodied Data Ingestion
    "https://arxiv.org/abs/2602.12275",  # On-Policy Context Distillation for Language Models
    "https://arxiv.org/abs/2602.12279",  # UniT: Unified Multimodal Chain-of-Thought Test-time Scaling
    "https://arxiv.org/abs/2602.12281",  # Scaling Verification Can Be More Effective than Scaling Policy Learning for Vision-Language-Action Alignment
    "https://arxiv.org/abs/2602.12322",  # ForeAct: Steering Your VLA with Efficient Visual Foresight Planning
    "https://arxiv.org/abs/2602.12385",  # Zero-Shot Adaptation to Robot Structural Damage via Natural Language-Informed Kinodynamics Modeling
    "https://arxiv.org/abs/2602.12395",  # What does RL improve for Visual Reasoning? A Frankenstein-Style Analysis
    "https://arxiv.org/abs/2602.12405",  # Self-Refining Vision Language Model for Robotic Failure Detection and Reasoning
    "https://arxiv.org/abs/2602.12628",  # Beyond Imitation: Reinforcement Learning-Based Sim-Real Co-Training for VLA Models
    "https://arxiv.org/abs/2602.13040",  # TCRL: Temporal-Coupled Adversarial Training for Robust Constrained Reinforcement Learning in Worst-Case Scenarios
    "https://arxiv.org/abs/2602.13052",  # Quantization-Aware Collaborative Inference for Large Embodied AI Models
    "https://arxiv.org/abs/2602.13086",  # UniManip: General-Purpose Zero-Shot Robotic Manipulation with Agentic Operational Graph
    "https://arxiv.org/abs/2602.13294",  # VisPhyWorld: Probing Physical Reasoning via Code-Driven Video Reconstruction
    "https://arxiv.org/abs/2602.13579",  # TactAlign: Human-to-Robot Policy Transfer via Tactile Alignment
    "https://arxiv.org/abs/2602.13656",  # A Kung Fu Athlete Bot That Can Do It All Day: Highly Dynamic, Balance-Challenging Motion Dataset and Autonomous Fall-Resilient Tracking
    "https://arxiv.org/abs/2602.13689",  # Symmetry-Aware Fusion of Vision and Tactile Sensing via Bilateral Force Priors for Robotic Manipulation
    "https://arxiv.org/abs/2602.13710",  # HBVLA: Pushing 1-Bit Post-Training Quantization for Vision-Language-Action Models
    "https://arxiv.org/abs/2602.13764",  # MOTIF: Learning Action Motifs for Few-shot Cross-Embodiment Transfer
    "https://arxiv.org/abs/2602.13810",  # Mean Flow Policy with Instantaneous Velocity Constraint for One-step Action Generation
    "https://arxiv.org/abs/2602.13850",  # Humanoid Hanoi: Investigating Shared Whole-Body Control for Skill-Based Box Rearrangement
    "https://arxiv.org/abs/2602.13949",  # Experiential Reinforcement Learning
    "https://arxiv.org/abs/2602.13977",  # WoVR: World Models as Reliable Simulators for Post-Training VLA Policies with RL
    "https://arxiv.org/abs/2602.14174",  # Direction Matters: Learning Force Direction Enables Sim-to-Real Contact-Rich Manipulation
    "https://arxiv.org/abs/2602.14351",  # WIMLE: Uncertainty-Aware World Models with IMLE for Sample-Efficient Continuous Control
    "https://arxiv.org/abs/2602.14697",  # Evolutionary System Prompt Learning for Reinforcement Learning in LLMs
    "https://arxiv.org/abs/2602.14926",  # MAC-AMP: A Closed-Loop Multi-Agent Collaboration System for Multi-Objective Antimicrobial Peptide Design
    "https://arxiv.org/abs/2602.15010",  # BPP: Long-Context Robot Imitation Learning by Focusing on Key History Frames
    "https://arxiv.org/abs/2602.15029",  # Symmetry in language statistics shapes the geometry of model representations
    "https://arxiv.org/abs/2602.15549",  # VLM-DEWM: Dynamic External World Model for Verifiable and Resilient Vision-Language Planning in Manufacturing
    "https://arxiv.org/abs/2602.15727",  # Spanning the Visual Analogy Space with a Weight Basis of LoRAs
    "https://arxiv.org/abs/2602.15733",  # MeshMimic: Geometry-Aware Humanoid Motion Learning through 3D Scene Reconstruction
    "https://arxiv.org/abs/2602.15817",  # Solving Parameter-Robust Avoid Problems with Unknown Feasibility using Reinforcement Learning
    "https://arxiv.org/abs/2602.15827",  # Perceptive Humanoid Parkour: Chaining Dynamic Human Skills via Motion Matching
    "https://arxiv.org/abs/2602.15918",  # EarthSpatialBench: Benchmarking Spatial Reasoning Capabilities of Multimodal LLMs on Earth Imagery
    "https://arxiv.org/abs/2602.15922",  # World Action Models are Zero-shot Policies
    "https://arxiv.org/abs/2602.15950",  # Can Vision-Language Models See Squares? Text-Recognition Mediates Spatial Reasoning Across Three Model Families
    "https://arxiv.org/abs/2602.15989",  # SAM 3D Body: Robust Full-Body Human Mesh Recovery
    "https://arxiv.org/abs/2602.16086",  # LGQ: Learning Discretization Geometry for Scalable and Stable Image Tokenization
    "https://arxiv.org/abs/2602.16182",  # World Model Failure Classification and Anomaly Detection for Autonomous Inspection
    "https://arxiv.org/abs/2602.16313",  # MemoryArena: Benchmarking Agent Memory in Interdependent Multi-Session Agentic Tasks
    "https://arxiv.org/abs/2602.16444",  # RoboGene: Boosting VLA Pre-training via Diversity-Driven Agentic Framework for Real-World Task Generation
    "https://arxiv.org/abs/2602.16511",  # VIGOR: Visual Goal-In-Context Inference for Unified Humanoid Fall Safety
    "https://arxiv.org/abs/2602.16548",  # RIDER: 3D RNA Inverse Design with Reinforcement Learning-Guided Diffusion
    "https://arxiv.org/abs/2602.16702",  # Saliency-Aware Multi-Route Thinking: Revisiting Vision-Language Reasoning
    "https://arxiv.org/abs/2602.16705",  # HERO: Learning Humanoid End-Effector Control for Visual Whole-Body Open-Vocabulary Object Grasping
    "https://arxiv.org/abs/2602.16710",  # EgoScale: Scaling Dexterous Manipulation with Diverse Egocentric Human Data
    "https://arxiv.org/abs/2602.16712",  # One Hand to Rule Them All: Canonical Representations for Unified Dexterous Manipulation
    "https://arxiv.org/abs/2602.16802",  # References Improve LLM Alignment in Non-Verifiable Domains
    "https://arxiv.org/abs/2602.16839",  # Training Large Reasoning Models Efficiently via Progressive Thought Encoding
    "https://arxiv.org/abs/2602.16863",  # SimToolReal: An Object-Centric Policy for Zero-Shot Dexterous Tool Manipulation
    "https://arxiv.org/abs/2602.17062",  # Retaining Suboptimal Actions to Follow Shifting Optima in Multi-Agent Reinforcement Learning
    "https://arxiv.org/abs/2602.17078",  # Safe Continuous-time Multi-Agent Reinforcement Learning via Epigraph Form
    "https://arxiv.org/abs/2602.17134",  # B$^3$-Seg: Camera-Free, Training-Free 3DGS Segmentation via Analytic EIG and Beta-Bernoulli Bayesian Updates
    "https://arxiv.org/abs/2602.17259",  # FRAPPE: Infusing World Modeling into Generalist Policies via Multiple Future Representation Alignment
    "https://arxiv.org/abs/2602.17270",  # Unified Latents (UL): How to train your latents
    "https://arxiv.org/abs/2602.17558",  # RetouchIQ: MLLM Agents for Instruction-Based Image Retouching with Generalist Reward
    "https://arxiv.org/abs/2602.17659",  # When Vision Overrides Language: Evaluating and Mitigating Counterfactual Failures in VLAs
    "https://arxiv.org/abs/2602.17807",  # VidEoMT: Your ViT is Secretly Also a Video Segmentation Model
    "https://arxiv.org/abs/2602.17921",  # Latent Diffeomorphic Co-Design of End-Effectors for Deformable and Fragile Object Manipulation
    "https://arxiv.org/abs/2602.17930",  # MIRA: Memory-Integrated Reinforcement Learning Agent with Limited LLM Guidance
    "https://arxiv.org/abs/2602.17951",  # ROCKET: Residual-Oriented Multi-Layer Alignment for Spatially-Aware Vision-Language-Action Models
    "https://arxiv.org/abs/2602.18015",  # Flow Actor-Critic for Offline Reinforcement Learning
    "https://arxiv.org/abs/2602.18025",  # Cross-Embodiment Offline Reinforcement Learning for Heterogeneous Robot Datasets
    "https://arxiv.org/abs/2602.18117",  # Flow Matching with Injected Noise for Offline-to-Online Reinforcement Learning
    "https://arxiv.org/abs/2602.18224",  # SimVLA: A Simple VLA Baseline for Robotic Manipulation
    "https://arxiv.org/abs/2602.18374",  # Zero-shot Interactive Perception
    "https://arxiv.org/abs/2602.18397",  # How Fast Can I Run My VLA? Demystifying VLA Inference Performance with VLA-Perf
    "https://arxiv.org/abs/2602.18532",  # VLANeXt: Recipes for Building Strong VLA Models
    "https://arxiv.org/abs/2602.18639",  # Learning Invariant Visual Representations for Planning with Joint-Embedding Predictive World Models
    "https://arxiv.org/abs/2602.18739",  # When World Models Dream Wrong: Physical-Conditioned Adversarial Attacks against World Models
    "https://arxiv.org/abs/2602.18884",  # TPRU: Advancing Temporal and Procedural Understanding in Large Multimodal Models
    "https://arxiv.org/abs/2602.18993",  # SeaCache: Spectral-Evolution-Aware Cache for Accelerating Diffusion Models
    "https://arxiv.org/abs/2602.19063",  # Direction-aware 3D Large Multimodal Models
    "https://arxiv.org/abs/2602.19083",  # ChordEdit: One-Step Low-Energy Transport for Image Editing
    "https://arxiv.org/abs/2602.19134",  # Mapping Networks
    "https://arxiv.org/abs/2602.19313",  # TOPReward: Token Probabilities as Hidden Zero-Shot Rewards for Robotics
    "https://arxiv.org/abs/2602.19764",  # Towards Dexterous Embodied Manipulation via Deep Multi-Sensory Fusion and Sparse Expert Scaling
    "https://arxiv.org/abs/2602.20057",  # AdaWorldPolicy: World-Model-Driven Diffusion Policy with Online Adaptive Learning for Robotic Manipulation
    "https://arxiv.org/abs/2602.20133",  # AdaEvolve: Adaptive LLM Driven Zeroth-Order Optimization
    "https://arxiv.org/abs/2602.20159",  # A Very Big Video Reasoning Suite
    "https://arxiv.org/abs/2602.20160",  # tttLRM: Test-Time Training for Long Context and Autoregressive 3D Reconstruction
    "https://arxiv.org/abs/2602.20197",  # Controllable Exploration in Hybrid-Policy RLVR for Multi-Modal Reasoning
    "https://arxiv.org/abs/2602.20200",  # Global Prior Meets Local Consistency: Dual-Memory Augmented Vision-Language-Action Model for Efficient Robotic Manipulation
    "https://arxiv.org/abs/2602.20220",  # What Matters for Simulation to Online Reinforcement Learning on Real Robots
    "https://arxiv.org/abs/2602.20309",  # QuantVLA: Scale-Calibrated Post-Training Quantization for Vision-Language-Action Models
    "https://arxiv.org/abs/2602.20363",  # Aesthetic Camera Viewpoint Suggestion with 3D Aesthetic Field
    "https://arxiv.org/abs/2602.20574",  # GATES: Self-Distillation under Privileged Context with Consensus Gating
    "https://arxiv.org/abs/2602.20630",  # From Pairs to Sequences: Track-Aware Policy Gradients for Keypoint Detection
    "https://arxiv.org/abs/2602.20687",  # How Foundational Skills Influence VLM-based Embodied Agents:A Native Perspective
    "https://arxiv.org/abs/2602.20722",  # Buffer Matters: Unleashing the Power of Off-Policy Reinforcement Learning in Large Language Model Reasoning
    "https://arxiv.org/abs/2602.20739",  # PyVision-RL: Forging Open Agentic Vision Models via RL
    "https://arxiv.org/abs/2602.20809",  # Regret-Guided Search Control for Efficient Learning in AlphaZero
    "https://arxiv.org/abs/2602.20901",  # SpatiaLQA: A Benchmark for Evaluating Spatial Logical Reasoning in Vision-Language Models
    "https://arxiv.org/abs/2602.20913",  # LongVideo-R1: Smart Navigation for Low-cost Long Video Understanding
    "https://arxiv.org/abs/2602.20980",  # CrystaL: Spontaneous Emergence of Visual Latents in MLLMs
    "https://arxiv.org/abs/2602.21015",  # From Perception to Action: An Interactive Benchmark for Vision Reasoning
    "https://arxiv.org/abs/2602.21054",  # VAUQ: Vision-Aware Uncertainty Quantification for LVLM Self-Evaluation
    "https://arxiv.org/abs/2602.21157",  # HALO: A Unified Vision-Language-Action Model for Embodied Multimodal Chain-of-Thought Reasoning
    "https://arxiv.org/abs/2602.21158",  # SELAUR: Self Evolving LLM Agent via Uncertainty-aware Rewards
    "https://arxiv.org/abs/2602.21172",  # NoRD: A Data-Efficient Vision-Language-Action Model that Drives without Reasoning
    "https://arxiv.org/abs/2602.21186",  # Spa3R: Predictive Spatial Field Modeling for 3D Visual Reasoning
    "https://arxiv.org/abs/2602.21198",  # Learning from Trials and Errors: Reflective Test-Time Planning for Embodied LLMs
    "https://arxiv.org/abs/2602.21346",  # Alignment-Weighted DPO: A principled reasoning approach to improve safety alignment
    "https://arxiv.org/abs/2602.21435",  # Synergizing Understanding and Generation with Interleaved Analyzing-Drafting Thinking
    "https://arxiv.org/abs/2602.21497",  # See It, Say It, Sorted: An Iterative Training-Free Framework for Visually-Grounded Multimodal Reasoning in LVLMs
    "https://arxiv.org/abs/2602.21531",  # LiLo-VLA: Compositional Long-Horizon Manipulation via Linked Object-Centric Policies
    "https://arxiv.org/abs/2602.21619",  # When More Is Less: A Systematic Analysis of Spatial and Commonsense Information for Visual Spatial Reasoning
    "https://arxiv.org/abs/2602.21628",  # RuCL: Stratified Rubric-Based Curriculum Learning for Multimodal Large Language Model Reasoning
    "https://arxiv.org/abs/2602.21633",  # Self-Correcting VLA: Online Action Refinement via Sparse World Imagination
    "https://arxiv.org/abs/2602.21655",  # CCCaption: Dual-Reward Reinforcement Learning for Complete and Correct Image Captioning
    "https://arxiv.org/abs/2602.21728",  # Explore-on-Graph: Incentivizing Autonomous Exploration of Large Language Models on Knowledge Graphs with Path-refined Reward Modeling
    "https://arxiv.org/abs/2602.21736",  # Joint-Aligned Latent Action: Towards Scalable VLA Pretraining in the Wild
    "https://arxiv.org/abs/2602.21919",  # Learning in the Null Space: Small Singular Values for Continual Learning
    "https://arxiv.org/abs/2602.21992",  # PanoEnv: Exploring 3D Spatial Intelligence in Panoramic Environments with Reinforcement Learning
    "https://arxiv.org/abs/2602.22010",  # World Guidance: World Modeling in Condition Space for Action Generation
    "https://arxiv.org/abs/2602.22225",  # SmartChunk Retrieval: Query-Aware Chunk Compression with Planning for Efficient Document RAG
    "https://arxiv.org/abs/2602.22461",  # EgoAVFlow: Robot Policy Learning with Active Vision from Human Egocentric Videos via 3D Flow
    "https://arxiv.org/abs/2602.22579",  # Metamorphic Testing of Vision-Language Action-Enabled Robots
    "https://arxiv.org/abs/2602.22663",  # Rethinking the Practicality of Vision-language-action Model: A Comprehensive Benchmark and An Improved Baseline
    "https://arxiv.org/abs/2602.22703",  # Enhancing Geometric Perception in VLMs via Translator-Guided Reinforcement Learning
    "https://arxiv.org/abs/2602.22766",  # Imagination Helps Visual Reasoning, But Not Yet in Latent Space
    "https://arxiv.org/abs/2602.22817",  # Hierarchy-of-Groups Policy Optimization for Long-Horizon Agentic Tasks
    "https://arxiv.org/abs/2602.22859",  # From Blind Spots to Gains: Diagnostic-Driven Iterative Training for Large Multimodal Models
    "https://arxiv.org/abs/2602.22896",  # DySL-VLA: Efficient Vision-Language-Action Model Inference via Dynamic-Static Layer-Skipping for Robot Manipulation
    "https://arxiv.org/abs/2602.22932",  # MSJoE: Jointly Evolving MLLM and Sampler for Efficient Long-Form Video Understanding
    "https://arxiv.org/abs/2602.23008",  # Exploratory Memory-Augmented LLM Agent via Hybrid On- and Off-Policy Optimization
    "https://arxiv.org/abs/2602.23024",  # InCoM: Intent-Driven Perception and Structured Coordination for Mobile Manipulation
    "https://arxiv.org/abs/2602.23058",  # GeoWorld: Geometric World Models
    "https://arxiv.org/abs/2602.23152",  # The Trinity of Consistency as a Defining Principle for General World Models
    "https://arxiv.org/abs/2602.23253",  # SPARR: Simulation-based Policies with Asymmetric Real-world Residuals for Assembly
    "https://arxiv.org/abs/2602.23320",  # ParamMem: Augmenting Language Agents with Parametric Reflective Memory
    "https://arxiv.org/abs/2602.23339",  # Retrieve and Segment: Are a Few Examples Enough to Bridge the Supervision Gap in Open-Vocabulary Segmentation?
    "https://arxiv.org/abs/2602.23413",  # EvoX: Meta-Evolution for Automated Discovery
    "https://arxiv.org/abs/2602.23615",  # Annotation-Free Visual Reasoning for High-Resolution Large Multimodal Models via Reinforcement Learning
    "https://arxiv.org/abs/2602.23648",  # FAVLA: A Force-Adaptive Fast-Slow VLA model for Contact-Rich Robotic Manipulation
    "https://arxiv.org/abs/2602.23759",  # Learning Accurate Segmentation Purely from Self-Supervision
    "https://arxiv.org/abs/2602.23770",  # MAGE: Multi-scale Autoregressive Generation for Offline Reinforcement Learning
    "https://arxiv.org/abs/2602.23802",  # EMO-R3: Reflective Reinforcement Learning for Emotional Reasoning in Multimodal Large Language Models
    "https://arxiv.org/abs/2602.23959",  # Thinking with Images as Continuous Actions: Numerical Visual Chain-of-Thought
    "https://arxiv.org/abs/2602.24041",  # Look Carefully: Adaptive Visual Reinforcements in Multimodal Large Language Models for Hallucination Mitigation
    "https://arxiv.org/abs/2602.24233",  # Enhancing Spatial Understanding in Image Generation via Reward Modeling
    "https://arxiv.org/abs/2602.24288",  # DARE-bench: Evaluating Modeling and Instruction Fidelity of LLMs in Data Science
    "https://arxiv.org/abs/2603.00110",  # Learning Physics from Pretrained Video Models: A Multimodal Continuous and Sequential World Interaction Models for Robotic Manipulation
    "https://arxiv.org/abs/2603.00136",  # TinyVLM: Zero-Shot Object Detection on Microcontrollers via Vision-Language Distillation with Matryoshka Embeddings
    "https://arxiv.org/abs/2603.00142",  # Evaluating Theory of Mind and Internal Beliefs in LLM-Based Multi-Agent Systems
    "https://arxiv.org/abs/2603.00182",  # Embedding Morphology into Transformers for Cross-Robot Policy Learning
    "https://arxiv.org/abs/2603.00207",  # VisRef: Visual Refocusing while Thinking Improves Test-Time Scaling in Multi-Modal Large Reasoning Models
    "https://arxiv.org/abs/2603.00461",  # ReMoT: Reinforcement Learning with Motion Contrast Triplets
    "https://arxiv.org/abs/2603.00515",  # MLLM-4D: Towards Visual-based Spatial-Temporal Intelligence
    "https://arxiv.org/abs/2603.00518",  # Vision-TTT: Efficient and Expressive Visual Representation Learning with Test-Time Training
    "https://arxiv.org/abs/2603.00526",  # Mesh-Pro: Asynchronous Advantage-guided Ranking Preference Optimization for Artist-style Quadrilateral Mesh Generation
    "https://arxiv.org/abs/2603.00716",  # Frozen Policy Iteration: Computationally Efficient RL under Linear $Q^π$ Realizability for Deterministic Dynamics
    "https://arxiv.org/abs/2603.00732",  # UniHM: Unified Dexterous Hand Manipulation with Vision Language Model
    "https://arxiv.org/abs/2603.00903",  # Principled Fast and Meta Knowledge Learners for Continual Reinforcement Learning
    "https://arxiv.org/abs/2603.00905",  # pySpatial: Generating 3D Visual Programs for Zero-Shot Spatial Reasoning
    "https://arxiv.org/abs/2603.01063",  # Unleashing VLA Potentials in Autonomous Driving via Explicit Learning from Failures
    "https://arxiv.org/abs/2603.01097",  # Understanding LoRA as Knowledge Memory: An Empirical Analysis
    "https://arxiv.org/abs/2603.01106",  # DIVA-GRPO: Enhancing Multimodal Reasoning through Difficulty-Adaptive Variant Advantage
    "https://arxiv.org/abs/2603.01142",  # ArtLLM: Generating Articulated Assets via 3D LLM
    "https://arxiv.org/abs/2603.01151",  # D-REX: Differentiable Real-to-Sim-to-Real Engine for Learning Dexterous Grasping
    "https://arxiv.org/abs/2603.01163",  # BeautyGRPO: Aesthetic Alignment for Face Retouching via Dynamic Path Guidance and Fine-Grained Preference Modeling
    "https://arxiv.org/abs/2603.01214",  # Reasoning Boosts Opinion Alignment in LLMs
    "https://arxiv.org/abs/2603.01228",  # Towards Policy-Adaptive Image Guardrail: Benchmark and Method
    "https://arxiv.org/abs/2603.01229",  # RMBench: Memory-Dependent Robotic Manipulation Benchmark with Insights into Policy Design
    "https://arxiv.org/abs/2603.01441",  # Unifying Language-Action Understanding and Generation for Autonomous Driving
    "https://arxiv.org/abs/2603.01631",  # Learning Thermal-Aware Locomotion Policies for an Electrically-Actuated Quadruped Robot
    "https://arxiv.org/abs/2603.01639",  # Learning to Draft: Adaptive Speculative Decoding with Reinforcement Learning
    "https://arxiv.org/abs/2603.01667",  # Chain-of-Context Learning: Dynamic Constraint Understanding for Multi-Task VRPs
    "https://arxiv.org/abs/2603.01694",  # MVR: Multi-view Video Reward Shaping for Reinforcement Learning
    "https://arxiv.org/abs/2603.01696",  # Cross-modal Identity Mapping: Minimizing Information Loss in Modality Conversion via Reinforcement Learning
    "https://arxiv.org/abs/2603.01741",  # Rethinking Policy Diversity in Ensemble Policy Gradient in Large-Scale Reinforcement Learning
    "https://arxiv.org/abs/2603.01771",  # Hyperparameter Trajectory Inference with Conditional Lagrangian Optimal Transport
    "https://arxiv.org/abs/2603.02008",  # Temporal Representations for Exploration: Learning Complex Exploratory Behavior without Extrinsic Rewards
    "https://arxiv.org/abs/2603.02091",  # Learning from Synthetic Data Improves Multi-hop Reasoning
    "https://arxiv.org/abs/2603.02115",  # Robometer: Scaling General-Purpose Robotic Reward Models via Trajectory Comparisons
    "https://arxiv.org/abs/2603.02146",  # LongRLVR: Long-Context Reinforcement Learning Requires Verifiable Context Rewards
    "https://arxiv.org/abs/2603.02188",  # Multi-Head Low-Rank Attention
    "https://arxiv.org/abs/2603.02203",  # Tool Verification for Test-Time Reinforcement Learning
    "https://arxiv.org/abs/2603.02224",  # Subspace Geometry Governs Catastrophic Forgetting in Low-Rank Adaptation
    "https://arxiv.org/abs/2603.02443",  # Safe Whole-Body Loco-Manipulation via Combined Model and Learning-based Control
    "https://arxiv.org/abs/2603.02511",  # Learning Object-Centric Spatial Reasoning for Sequential Manipulation in Cluttered Environments
    "https://arxiv.org/abs/2603.02556",  # Through the Lens of Contrast: Self-Improving Visual Reasoning in VLMs
    "https://arxiv.org/abs/2603.02772",  # Agentic Self-Evolutionary Replanning for Embodied Navigation
    "https://arxiv.org/abs/2603.02908",  # SAE as a Crystal Ball: Interpretable Features Predict Cross-domain Transferability of LLMs without Training
    "https://arxiv.org/abs/2603.02951",  # CGL: Advancing Continual GUI Learning via Reinforcement Fine-Tuning
    "https://arxiv.org/abs/2603.02959",  # Semi-Supervised Few-Shot Adaptation of Vision-Language Models
    "https://arxiv.org/abs/2603.03026",  # Any Resolution Any Geometry: From Multi-View To Multi-Patch
    "https://arxiv.org/abs/2603.03067",  # CMoE: Contrastive Mixture of Experts for Motion Control and Terrain Adaptation of Humanoid Robots
    "https://arxiv.org/abs/2603.03072",  # TikZilla: Scaling Text-to-TikZ with High-Quality Data and Reinforcement Learning
    "https://arxiv.org/abs/2603.03195",  # Chain of World: World Model Thinking in Latent Motion
    "https://arxiv.org/abs/2603.03197",  # Specificity-aware reinforcement learning for fine-grained open-world classification
    "https://arxiv.org/abs/2603.03241",  # UniG2U-Bench: Do Unified Models Advance Multimodal Understanding?
    "https://arxiv.org/abs/2603.03243",  # HoMMI: Learning Whole-Body Mobile Manipulation from Human Demonstrations
    "https://arxiv.org/abs/2603.03276",  # Beyond Language Modeling: An Exploration of Multimodal Pretraining
    "https://arxiv.org/abs/2603.03279",  # ULTRA: Unified Multimodal Control for Autonomous Humanoid Whole-Body Loco-Manipulation
    "https://arxiv.org/abs/2603.03380",  # LiteVLA-Edge: Quantized On-Device Multimodal Control for Embedded Robotics
    "https://arxiv.org/abs/2603.03482",  # Beyond Pixel Histories: World Models with Persistent 3D State
    "https://arxiv.org/abs/2603.03485",  # Phys4D: Fine-Grained Physics-Consistent 4D Modeling from Video Diffusion
    "https://arxiv.org/abs/2603.03505",  # PhyPrompt: RL-based Prompt Refinement for Physically Plausible Text-to-Video Generation
    "https://arxiv.org/abs/2603.03596",  # MEM: Multi-Scale Embodied Memory for Vision Language Action Models
    "https://arxiv.org/abs/2603.03818",  # Pretrained Vision-Language-Action Models are Surprisingly Resistant to Forgetting in Continual Learning
    "https://arxiv.org/abs/2603.03836",  # SkillVLA: Tackling Combinatorial Diversity in Dual-Arm Manipulation via Skill Reuse
    "https://arxiv.org/abs/2603.03857",  # DeepScan: A Training-Free Framework for Visually Grounded Reasoning in Large Vision-Language Models
    "https://arxiv.org/abs/2603.03944",  # Spatial Causal Prediction in Video
    "https://arxiv.org/abs/2603.04002",  # Discriminative Perception via Anchored Description for Reasoning Segmentation
    "https://arxiv.org/abs/2603.04029",  # Self-adapting Robotic Agents through Online Continual Reinforcement Learning with World Model Feedback
    "https://arxiv.org/abs/2603.04071",  # SaFeR: Safety-Critical Scenario Generation for Autonomous Driving Test via Feasibility-Constrained Token Resampling
    "https://arxiv.org/abs/2603.04333",  # What Does Flow Matching Bring To TD Learning?
    "https://arxiv.org/abs/2603.04531",  # PTLD: Sim-to-real Privileged Tactile Latent Distillation for Dexterous Manipulation
    "https://arxiv.org/abs/2603.04560",  # From Local Corrections to Generalized Skills: Improving Neuro-Symbolic Policies with MEMO
    "https://arxiv.org/abs/2603.04639",  # RoboMME: Benchmarking and Understanding Memory for Robotic Generalist Policies
    "https://arxiv.org/abs/2603.04948",  # $\nabla$-Reasoner: LLM Reasoning via Test-Time Gradient Descent in Latent Space
    "https://arxiv.org/abs/2603.05044",  # WebFactory: Automated Compression of Foundational Language Intelligence into Grounded Web Agents
    "https://arxiv.org/abs/2603.05147",  # Act, Think or Abstain: Complexity-Aware Adaptive Inference for Vision-Language-Action Models
    "https://arxiv.org/abs/2603.05218",  # KARL: Knowledge Agents via Reinforcement Learning
    "https://arxiv.org/abs/2603.05225",  # AI+HW 2035: Shaping the Next Decade
    "https://arxiv.org/abs/2603.05256",  # Wiki-R1: Incentivizing Multimodal Reasoning for Knowledge-based VQA via Data and Sampling Curriculum
    "https://arxiv.org/abs/2603.05410",  # PhysiFlow: Physics-Aware Humanoid Whole-Body VLA via Multi-Brain Latent Flow Matching and Robust Tracking
    "https://arxiv.org/abs/2603.05438",  # Planning in 8 Tokens: A Compact Discrete Tokenizer for Latent World Model
    "https://arxiv.org/abs/2603.05449",  # RealWonder: Real-Time Physical Action-Conditioned Video Generation
    "https://arxiv.org/abs/2603.05687",  # Contact-Grounded Policy: Dexterous Visuotactile Policy with Generative Contact Grounding
    "https://arxiv.org/abs/2603.05815",  # Hierarchical Latent Action Model
    "https://arxiv.org/abs/2603.05900",  # Reference-guided Policy Optimization for Molecular Optimization via LLM Reasoning
    "https://arxiv.org/abs/2603.06043",  # Learning to Generate via Understanding: Understanding-Driven Intrinsic Rewarding for Unified Multimodal Models
    "https://arxiv.org/abs/2603.06408",  # Physical Simulator In-the-Loop Video Generation
    "https://arxiv.org/abs/2603.06569",  # Penguin-VL: Exploring the Efficiency Limits of VLM with LLM-based Vision Encoders
    "https://arxiv.org/abs/2603.06693",  # Soft Equivariance Regularization for Invariant Self-Supervised Learning
    "https://arxiv.org/abs/2603.06987",  # Foundational World Models Accurately Detect Bimanual Manipulator Failures
    "https://arxiv.org/abs/2603.07020",  # RESCHED: Rethinking Flexible Job Shop Scheduling from a Transformer-based Architecture with Simplified States
    "https://arxiv.org/abs/2603.07079",  # Entropy-Aware On-Policy Distillation of Language Models
    "https://arxiv.org/abs/2603.07197",  # $\textbf{Re}^{2}$: Unlocking LLM Reasoning via Reinforcement Learning with Re-solving
    "https://arxiv.org/abs/2603.07335",  # VisualScratchpad: Inference-time Visual Concepts Analysis in Vision Language Models
    "https://arxiv.org/abs/2603.07642",  # Helix: Evolutionary Reinforcement Learning for Open-Ended Scientific Problem Solving
    "https://arxiv.org/abs/2603.07648",  # AtomicVLA: Unlocking the Potential of Atomic Skill Learning in Robots
    "https://arxiv.org/abs/2603.07799",  # MWM: Mobile World Models for Action-Conditioned Consistent Prediction
    "https://arxiv.org/abs/2603.07904",  # DyQ-VLA: Temporal-Dynamic-Aware Quantization for Embodied Vision-Language-Action Models
    "https://arxiv.org/abs/2603.08021",  # AffordGrasp: Cross-Modal Diffusion for Affordance-Aware Grasp Synthesis
    "https://arxiv.org/abs/2603.08055",  # Speed3R: Sparse Feed-forward 3D Reconstruction Models
    "https://arxiv.org/abs/2603.08118",  # Model-based Offline RL via Robust Value-Aware Model Learning with Implicitly Differentiable Adaptive Weighting
    "https://arxiv.org/abs/2603.08342",  # PhaForce: Phase-Scheduled Visual-Force Policy Learning with Slow Planning and Fast Correction for Contact-Rich Manipulation
    "https://arxiv.org/abs/2603.08403",  # SPIRAL: A Closed-Loop Framework for Self-Improving Action World Models via Reflective Planning Agents
    "https://arxiv.org/abs/2603.08541",  # EquiBim: Learning Symmetry-Equivariant Policy for Bimanual Manipulation
    "https://arxiv.org/abs/2603.08546",  # Interactive World Simulator for Robot Policy Training and Evaluation
    "https://arxiv.org/abs/2603.08561",  # RetroAgent: From Solving to Evolving via Retrospective Dual Intrinsic Feedback
    "https://arxiv.org/abs/2603.08572",  # MetaWorld-X: Hierarchical World Modeling via VLM-Orchestrated Experts for Humanoid Loco-Manipulation
    "https://arxiv.org/abs/2603.08619",  # Embedding Classical Balance Control Principles in Reinforcement Learning for Humanoid Recovery
    "https://arxiv.org/abs/2603.08660",  # How Far Can Unsupervised RLVR Scale LLM Training?
    "https://arxiv.org/abs/2603.08961",  # FAME: Force-Adaptive RL for Expanding the Manipulation Envelope of a Full-Scale Humanoid
    "https://arxiv.org/abs/2603.09030",  # PlayWorld: Learning Robot World Models from Autonomous Play
    "https://arxiv.org/abs/2603.09079",  # GST-VLA: Structured Gaussian Spatial Tokens for 3D Depth-Aware Vision-Language-Action Models
    "https://arxiv.org/abs/2603.09094",  # Chain of Event-Centric Causal Thought for Physically Plausible Video Generation
    "https://arxiv.org/abs/2603.09206",  # MM-Zero: Self-Evolving Multi-Model Vision Language Models From Zero Data
    "https://arxiv.org/abs/2603.09292",  # See, Plan, Rewind: Progress-Aware Vision-Language-Action Models for Robust Robotic Manipulation
    "https://arxiv.org/abs/2603.09298",  # CORAL: Scalable Multi-Task Robot Learning via LoRA Experts
    "https://arxiv.org/abs/2603.09326",  # OddGridBench: Exposing the Lack of Fine-Grained Visual Discrepancy Sensitivity in Multimodal Large Language Models
    "https://arxiv.org/abs/2603.09513",  # Beyond Short-Horizon: VQ-Memory for Robust Long-Horizon Manipulation in Non-Markovian Simulation Benchmarks
    "https://arxiv.org/abs/2603.09956",  # Kinodynamic Motion Retargeting for Humanoid Locomotion via Multi-Contact Whole-Body Trajectory Optimization
    "https://arxiv.org/abs/2603.10052",  # OmniGuide: Universal Guidance Fields for Enhancing Generalist Robot Policies
    "https://arxiv.org/abs/2603.10158",  # Cross-Hand Latent Representation for Vision-Language-Action Models
    "https://arxiv.org/abs/2603.10160",  # ReMix: Reinforcement routing for mixtures of LoRAs in LLM finetuning
    "https://arxiv.org/abs/2603.10422",  # World2Act: Latent Action Post-Training via Skill-Compositional World Models
    "https://arxiv.org/abs/2603.10448",  # DiT4DiT: Jointly Modeling Video Dynamics and Actions for Generalizable Robot Control
    "https://arxiv.org/abs/2603.10675",  # Cybo-Waiter: A Physical Agentic Framework for Humanoid Whole-Body Locomotion-Manipulation
    "https://arxiv.org/abs/2603.10887",  # Dynamics-Predictive Sampling for Active RL Finetuning of Large Reasoning Models
    "https://arxiv.org/abs/2603.11106",  # RC-NF: Robot-Conditioned Normalizing Flow for Real-Time Anomaly Detection in Robotic Manipulation
    "https://arxiv.org/abs/2603.11327",  # Meta-Reinforcement Learning with Self-Reflection for Agentic Search
    "https://arxiv.org/abs/2603.11346",  # Learning to Assist: Physics-Grounded Human-Human Control via Multi-Agent Reinforcement Learning
    "https://arxiv.org/abs/2603.11600",  # Hybrid Energy-Aware Reward Shaping: A Unified Lightweight Physics-Guided Methodology for Policy Optimization
    "https://arxiv.org/abs/2603.11653",  # Simple Recipe Works: Vision-Language-Action Models are Natural Continual Learners with Reinforcement Learning
    "https://arxiv.org/abs/2603.11682",  # Entropy-Preserving Reinforcement Learning
    "https://arxiv.org/abs/2603.11691",  # STAIRS-Former: Spatio-Temporal Attention with Interleaved Recursive Structure Transformer for Offline Multi-task Multi-agent Reinforcement Learning
    "https://arxiv.org/abs/2603.12011",  # Can RL Improve Generalization of LLM Agents? An Empirical Study
    "https://arxiv.org/abs/2603.12056",  # XSkill: Continual Learning from Experience and Skills in Multimodal Agents
    "https://arxiv.org/abs/2603.12087",  # Cross-Domain Policy Optimization via Bellman Consistency and Hybrid Critics
    "https://arxiv.org/abs/2603.12149",  # Linking Perception, Confidence and Accuracy in MLLMs
    "https://arxiv.org/abs/2603.12185",  # ComFree-Sim: A GPU-Parallelized Analytical Contact Physics Engine for Scalable Contact-Rich Robotics Simulation and Control
    "https://arxiv.org/abs/2603.12193",  # SaPaVe: Towards Active Perception and Manipulation in Vision-Language-Action Models for Robotics
    "https://arxiv.org/abs/2603.12217",  # Real-World Point Tracking with Verifier-Guided Pseudo-Labeling
    "https://arxiv.org/abs/2603.12228",  # Neural Thickets: Diverse Task Experts Are Dense Around Pretrained Weights
    "https://arxiv.org/abs/2603.12231",  # Temporal Straightening for Latent Planning
    "https://arxiv.org/abs/2603.12248",  # Matching Features, Not Tokens: Energy-Based Fine-Tuning of Language Models
    "https://arxiv.org/abs/2603.12254",  # Attend Before Attention: Efficient and Scalable Video Understanding via Autoregressive Gazing
    "https://arxiv.org/abs/2603.12263",  # $Ψ_0$: An Open Foundation Model Towards Universal Humanoid Loco-Manipulation
    "https://arxiv.org/abs/2603.12382",  # SPARROW: Learning Spatial Precision and Temporal Referential Consistency in Pixel-Grounded Video MLLMs
    "https://arxiv.org/abs/2603.12510",  # Red-Teaming Vision-Language-Action Models via Quality Diversity Prompt Generation for Robust Robot Policies
    "https://arxiv.org/abs/2603.12553",  # Beyond Dense Futures: World Models as Structured Planners for Robotic Manipulation
    "https://arxiv.org/abs/2603.12595",  # Swap-guided Preference Learning for Personalized Reinforcement Learning from Human Feedback
    "https://arxiv.org/abs/2603.12639",  # RoboStereo: Dual-Tower 4D Embodied World Models for Unified Policy Optimization
    "https://arxiv.org/abs/2603.12665",  # TacVLA: Contact-Aware Tactile Fusion for Robust Vision-Language-Action Manipulation
    "https://arxiv.org/abs/2603.12730",  # AnchorVLA4D: an Anchor-Based Spatial-Temporal Vision-Language-Action Model for Robotic Manipulation
    "https://arxiv.org/abs/2603.12772",  # PVI: Plug-in Visual Injection for Vision-Language-Action Models
    "https://arxiv.org/abs/2603.12939",  # RoboStream: Weaving Spatio-Temporal Reasoning with Memory in Vision-Language Models for Robotics
    "https://arxiv.org/abs/2603.12942",  # ReMem-VLA: Empowering Vision-Language-Action Model with Memory via Dual-Level Recurrent Queries
    "https://arxiv.org/abs/2603.13033",  # ESPIRE: A Diagnostic Benchmark for Embodied Spatial Reasoning of Vision-Language Models
    "https://arxiv.org/abs/2603.13292",  # Pragma-VL: Towards a Pragmatic Arbitration of Safety and Helpfulness in MLLMs
    "https://arxiv.org/abs/2603.13348",  # AutoTool: Automatic Scaling of Tool-Use Capabilities in RL via Decoupled Entropy Constraints
    "https://arxiv.org/abs/2603.13528",  # Learning Actionable Manipulation Recovery via Counterfactual Failure Synthesis
    "https://arxiv.org/abs/2603.13616",  # Beyond Binary Success: Sample-Efficient and Statistically Rigorous Robot Policy Comparison
    "https://arxiv.org/abs/2603.13707",  # REFINE-DP: Diffusion Policy Fine-tuning for Humanoid Loco-manipulation via Reinforcement Learning
    "https://arxiv.org/abs/2603.13770",  # PhysAlign: Physics-Coherent Image-to-Video Generation through Feature and 3D Representation Alignment
    "https://arxiv.org/abs/2603.13825",  # Building Explicit World Model for Zero-Shot Open-World Object Manipulation
    "https://arxiv.org/abs/2603.13888",  # Path-conditioned Reinforcement Learning-based Local Planning for Long-Range Navigation
    "https://arxiv.org/abs/2603.13925",  # SmoothVLA: Aligning Vision-Language-Action Models with Physical Constraints via Intrinsic Smoothness Optimization
    "https://arxiv.org/abs/2603.13966",  # vla-eval: A Unified Evaluation Harness for Vision-Language-Action Models
    "https://arxiv.org/abs/2603.14010",  # URDF-Anything+: End-to-End Generation for Simulation-Ready Articulated Assets
    "https://arxiv.org/abs/2603.14117",  # Improving Visual Reasoning with Iterative Evidence Refinement
    "https://arxiv.org/abs/2603.14145",  # MMOU: A Massive Multi-Task Omni Understanding and Reasoning Benchmark for Long and Complex Real-World Videos
    "https://arxiv.org/abs/2603.14245",  # GoldenStart: Q-Guided Priors and Entropy Control for Distilling Flow Policies
    "https://arxiv.org/abs/2603.14308",  # Load-Aware Locomotion Control for Humanoid Robots in Industrial Transportation Tasks
    "https://arxiv.org/abs/2603.14327",  # OmniClone: Engineering a Robust, All-Rounder Whole-Body Humanoid Teleoperation System
    "https://arxiv.org/abs/2603.14482",  # V-JEPA 2.1: Unlocking Dense Features in Video Self-Supervised Learning
    "https://arxiv.org/abs/2603.14497",  # WorldVLM: Combining World Model Forecasting and Vision-Language Reasoning
    "https://arxiv.org/abs/2603.14498",  # R3DP: Real-Time 3D-Aware Policy for Embodied Manipulation
    "https://arxiv.org/abs/2603.14522",  # One-Policy-Fits-All: Geometry-Aware Action Latents for Cross-Embodiment Manipulation
    "https://arxiv.org/abs/2603.14609",  # GroundSet: A Cadastral-Grounded Dataset for Spatial Understanding with Vector Data
    "https://arxiv.org/abs/2603.14851",  # AutoMoT: A Unified Vision-Language-Action Model with Asynchronous Mixture-of-Transformers for End-to-End Autonomous Driving
    "https://arxiv.org/abs/2603.15031",  # Attention Residuals
    "https://arxiv.org/abs/2603.15169",  # ForceVLA2: Unleashing Hybrid Force-Position Control with Force Awareness for Contact-Rich Manipulation
    "https://arxiv.org/abs/2603.15255",  # SAGE: Multi-Agent Self-Evolution for LLM Reasoning
    "https://arxiv.org/abs/2603.15257",  # HapticVLA: Contact-Rich Manipulation via Vision-Language-Action Model without Inference-Time Tactile Sensing
    "https://arxiv.org/abs/2603.15359",  # NavThinker: Action-Conditioned World Models for Coupled Prediction and Planning in Social Navigation
    "https://arxiv.org/abs/2603.15381",  # Why AI systems don't learn and what to do about it: Lessons on autonomous learning from cognitive science
    "https://arxiv.org/abs/2603.15386",  # RieMind: Geometry-Grounded Spatial Agent for Scene Understanding
    "https://arxiv.org/abs/2603.15469",  # RoCo Challenge at AAAI 2026: Benchmarking Robotic Collaborative Manipulation for Assembly Towards Industrial Automation
    "https://arxiv.org/abs/2603.15546",  # Kimodo: Scaling Controllable Human Motion Generation
    "https://arxiv.org/abs/2603.15553",  # Self-Distillation of Hidden Layers for Self-Supervised Representation Learning
    "https://arxiv.org/abs/2603.15600",  # From Passive Observer to Active Critic: Reinforcement Learning Elicits Process Reasoning for Robotic Manipulation
    "https://arxiv.org/abs/2603.15616",  # GlyphPrinter: Region-Grouped Direct Preference Optimization for Glyph-Accurate Visual Text Rendering
    "https://arxiv.org/abs/2603.15619",  # Mixture-of-Depths Attention
    "https://arxiv.org/abs/2603.15759",  # Simulation Distillation: Pretraining World Models in Simulation for Rapid Real-World Adaptation
    "https://arxiv.org/abs/2603.15771",  # CorrectionPlanner: Self-Correction Planner with Reinforcement Learning in Autonomous Driving
    "https://arxiv.org/abs/2603.15789",  # Emergent Dexterity via Diverse Resets and Large-Scale Reinforcement Learning
    "https://arxiv.org/abs/2603.15956",  # ExpertGen: Scalable Sim-to-Real Expert Policy Learning from Imperfect Behavior Priors
    "https://arxiv.org/abs/2603.15958",  # Deriving Hyperparameter Scaling Laws via Modern Optimization Theory
    "https://arxiv.org/abs/2603.15975",  # UMO: Unified In-Context Learning Unlocks Motion Foundation Model Priors
    "https://arxiv.org/abs/2603.16151",  # EFF-Grasp: Energy-Field Flow Matching for Physics-Aware Dexterous Grasp Generation
    "https://arxiv.org/abs/2603.16195",  # S-VAM: Shortcut Video-Action Model by Self-Distilling Geometric and Semantic Foresight
    "https://arxiv.org/abs/2603.16253",  # Grounding the Score: Explicit Visual Premise Verification for Reliable Vision-Language Process Reward Models
    "https://arxiv.org/abs/2603.16368",  # Encoding Predictability and Legibility for Style-Conditioned Diffusion Policy
    "https://arxiv.org/abs/2603.16506",  # VIEW2SPACE: Studying Multi-View Visual Reasoning from Sparse Observations
    "https://arxiv.org/abs/2603.16666",  # Fast-WAM: Do World Action Models Need Test-time Future Imagination?
    "https://arxiv.org/abs/2603.16769",  # GDPO-SR: Group Direct Preference Optimization for One-Step Generative Image Super-Resolution
    "https://arxiv.org/abs/2603.16790",  # InCoder-32B: Code Foundation Model for Industrial Scenarios
    "https://arxiv.org/abs/2603.16806",  # DexGrasp-Zero: A Morphology-Aligned Policy for Zero-Shot Cross-Embodiment Dexterous Grasping
    "https://arxiv.org/abs/2603.16856",  # Online Experiential Learning for Language Models
    "https://arxiv.org/abs/2603.16860",  # DreamPlan: Efficient Reinforcement Fine-Tuning of Vision-Language Planners via Video World Models
    "https://arxiv.org/abs/2603.16861",  # MolmoB0T: Large-Scale Simulation Enables Zero-Shot Manipulation
    "https://arxiv.org/abs/2603.16870",  # Demystifing Video Reasoning
    "https://arxiv.org/abs/2603.16871",  # WorldCam: Interactive Autoregressive 3D Gaming Worlds with Camera Pose as a Unifying Geometric Representation
    "https://arxiv.org/abs/2603.17051",  # Astrolabe: Steering Forward-Process Reinforcement Learning for Distilled Autoregressive Video Models
    "https://arxiv.org/abs/2603.17063",  # Transformers are Bayesian Networks
    "https://arxiv.org/abs/2603.17117",  # MosaicMem: Hybrid Spatial Memory for Controllable Video World Models
    "https://arxiv.org/abs/2603.17240",  # GigaWorld-Policy: An Efficient Action-Centered World--Action Model
    "https://arxiv.org/abs/2603.17305",  # Contrastive Reasoning Alignment: Reinforcement Learning from Hidden Representations
    "https://arxiv.org/abs/2603.17312",  # Recurrent Reasoning with Vision-Language Models for Estimating Long-Horizon Embodied Task Progress
    "https://arxiv.org/abs/2603.17541",  # Temporal Gains, Spatial Costs: Revisiting Video Fine-Tuning in Multimodal Large Language Models
    "https://arxiv.org/abs/2603.17621",  # Complementary Reinforcement Learning
    "https://arxiv.org/abs/2603.17655",  # Interpretable Cross-Domain Few-Shot Learning with Rectified Target-Domain Local Alignment
    "https://arxiv.org/abs/2603.17684",  # Does YOLO Really Need to See Every Training Image in Every Epoch?
    "https://arxiv.org/abs/2603.17693",  # Learning Transferable Temporal Primitives for Video Reasoning via Synthetic Videos
    "https://arxiv.org/abs/2603.17729",  # SARE: Sample-wise Adaptive Reasoning for Training-free Fine-grained Visual Recognition
    "https://arxiv.org/abs/2603.17808",  # EVA: Aligning Video World Models with Executable Robot Actions via Inverse Dynamics Rewards
    "https://arxiv.org/abs/2603.17851",  # DexViTac: Collecting Human Visuo-Tactile-Kinematic Demonstrations for Contact-Rich Dexterous Manipulation
    "https://arxiv.org/abs/2603.18091",  # Action Draft and Verify: A Self-Verifying Framework for Vision-Language-Action Model
    "https://arxiv.org/abs/2603.18202",  # R2-Dreamer: Redundancy-Reduced World Models without Decoders or Augmentation
    "https://arxiv.org/abs/2603.18336",  # ManiDreams: An Open-Source Library for Robust Object Manipulation via Uncertainty-aware Task-specific Intuitive Physics
    "https://arxiv.org/abs/2603.18494",  # MemoAct: Atkinson-Shiffrin-Inspired Memory-Augmented Visuomotor Policy for Robotic Manipulation
    "https://arxiv.org/abs/2603.18524",  # 3DreamBooth: High-Fidelity 3D Subject-Driven Video Generation Model
    "https://arxiv.org/abs/2603.18639",  # PhysVideo: Physically Plausible Video Generation with Cross-View Geometry Guidance
    "https://arxiv.org/abs/2603.18656",  # Balanced Thinking: Improving Chain of Thought Training in Vision Language Models
    "https://arxiv.org/abs/2603.18743",  # Memento-Skills: Let Agents Design Agents
    "https://arxiv.org/abs/2603.18886",  # Reasoning over mathematical objects: on-policy reward modeling and test time aggregation
    "https://arxiv.org/abs/2603.18892",  # MultihopSpatial: Multi-hop Compositional Spatial Reasoning Benchmark for Vision-Language Model
    "https://arxiv.org/abs/2603.18979",  # PRIOR: Perceptive Learning for Humanoid Locomotion with Reference Gait Priors
    "https://arxiv.org/abs/2603.18991",  # CRAFT: Aligning Diffusion Models with Fine-Tuning Is Easier Than You Think
    "https://arxiv.org/abs/2603.19131",  # From Inference Efficiency to Embodied Efficiency: Revisiting Efficiency Metrics for Vision-Language-Action Models
    "https://arxiv.org/abs/2603.19137",  # GSMem: 3D Gaussian Splatting as Persistent Spatial Memory for Zero-Shot Embodied Exploration and Reasoning
    "https://arxiv.org/abs/2603.19201",  # OmniVTA: Visuo-Tactile World Modeling for Contact-Rich Robotic Manipulation
    "https://arxiv.org/abs/2603.19227",  # Bridging Semantic and Kinematic Conditions with Diffusion-based Discrete Motion Tokenizer
    "https://arxiv.org/abs/2603.19231",  # MonoArt: Progressive Structural Reasoning for Monocular Articulated 3D Reconstruction
    "https://arxiv.org/abs/2603.19235",  # Generation Models Know Space: Unleashing Implicit 3D Priors for Scene Understanding
    "https://arxiv.org/abs/2603.19266",  # Probing to Refine: Reinforcement Distillation of LLMs via Explanatory Inversion
    "https://arxiv.org/abs/2603.19312",  # LeWorldModel: Stable End-to-End Joint-Embedding Predictive Architecture from Pixels
    "https://arxiv.org/abs/2603.19370",  # VAMPO: Policy Optimization for Improving Visual Dynamics in Video Action Models
    "https://arxiv.org/abs/2603.19461",  # Hyperagents
    "https://arxiv.org/abs/2603.19607",  # Physion-Eval: Evaluating Physical Realism in Generated Video via Human Reasoning
    "https://arxiv.org/abs/2603.19835",  # FIPO: Eliciting Deep Reasoning with Future-KL Influenced Policy Optimization
    "https://arxiv.org/abs/2603.20111",  # Var-JEPA: A Variational Formulation of the Joint-Embedding Predictive Architecture -- Bridging Predictive and Generative Self-Supervised Learning
    "https://arxiv.org/abs/2603.20147",  # AGILE: A Comprehensive Workflow for Humanoid Loco-Manipulation Learning
    "https://arxiv.org/abs/2603.20236",  # EnergyAction: Unimanual to Bimanual Composition with Energy-Based Models
    "https://arxiv.org/abs/2603.20278",  # OpenResearcher: A Fully Open Pipeline for Long-Horizon Deep Research Trajectory Synthesis
    "https://arxiv.org/abs/2603.21104",  # CounterScene: Counterfactual Causal Reasoning in Generative World Models for Safety-Critical Closed-Loop Evaluation
    "https://arxiv.org/abs/2603.21138",  # Incentivizing Generative Zero-Shot Learning via Outcome-Reward Reinforcement Learning with Visual Cues
    "https://arxiv.org/abs/2603.21175",  # Reward Sharpness-Aware Fine-Tuning for Diffusion Models
    "https://arxiv.org/abs/2603.21191",  # On the Role of Batch Size in Stochastic Conditional Gradient Methods
    "https://arxiv.org/abs/2603.21383",  # PivotRL: High Accuracy Agentic Post-Training at Low Compute Cost
    "https://arxiv.org/abs/2603.22003",  # VP-VLA: Visual Prompting as an Interface for Vision-Language-Action Models
    "https://arxiv.org/abs/2603.22057",  # SpatialBoost: Enhancing Visual Representation through Language-Guided Reasoning
    "https://arxiv.org/abs/2603.22078",  # Do World Action Models Generalize Better than VLAs? A Robustness Study
    "https://arxiv.org/abs/2603.22117",  # On the Direction of RLVR Updates for LLM Reasoning: Identification and Exploitation
    "https://arxiv.org/abs/2603.22126",  # ROBOGATE: Adaptive Failure Discovery for Safe Robot Policy Deployment via Two-Stage Boundary-Focused Sampling
    "https://arxiv.org/abs/2603.22187",  # Seeing is Improving: Visual Feedback for Iterative Text Layout Refinement
    "https://arxiv.org/abs/2603.22201",  # Make Tracking Easy: Neural Motion Retargeting for Humanoid Whole-body Control
    "https://arxiv.org/abs/2603.22212",  # Omni-WorldBench: Towards a Comprehensive Interaction-Centric Evaluation for World Models
    "https://arxiv.org/abs/2603.22228",  # SpatialReward: Verifiable Spatial Reward Modeling for Fine-Grained Spatial Consistency in Text-to-Image Generation
    "https://arxiv.org/abs/2603.22264",  # UniDex: A Robot Foundation Suite for Universal Dexterous Hand Control from Egocentric Human Videos
    "https://arxiv.org/abs/2603.22275",  # Repurposing Geometric Foundation Models for Multi-view Diffusion
    "https://arxiv.org/abs/2603.22279",  # 3D-Layout-R1: Structured Reasoning for Language-Instructed Spatial Editing
    "https://arxiv.org/abs/2603.22281",  # ThinkJEPA: Empowering Latent World Models with Large Vision-Language Reasoning Model
    "https://arxiv.org/abs/2603.22293",  # TIPS: Turn-Level Information-Potential Reward Shaping for Search-Augmented LLMs
    "https://arxiv.org/abs/2603.22387",  # Efficient Universal Perception Encoder
    "https://arxiv.org/abs/2603.22435",  # CaP-X: A Framework for Benchmarking and Improving Coding Agents for Robot Manipulation
    "https://arxiv.org/abs/2603.22446",  # Sparse but Critical: A Token-Level Analysis of Distributional Shifts in RLVR Fine-Tuning of LLMs
    "https://arxiv.org/abs/2603.22570",  # CanViT: Toward Active-Vision Foundation Models
    "https://arxiv.org/abs/2603.22574",  # GIFT: Generalizing Intent for Flexible Test-Time Rewards
    "https://arxiv.org/abs/2603.22703",  # Learning Safe-Stoppability Monitors for Humanoid Robots
    "https://arxiv.org/abs/2603.22760",  # SG-VLA: Learning Spatially-Grounded Vision-Language-Action Models for Mobile Manipulation
    "https://arxiv.org/abs/2603.22815",  # Focus, Don't Prune: Identifying Instruction-Relevant Regions for Information-Rich Image Understanding
    "https://arxiv.org/abs/2603.22847",  # Rethinking Token-Level Policy Optimization for Multimodal Chain-of-Thought
    "https://arxiv.org/abs/2603.22862",  # The Evolution of Tool Use in LLM Agents: From Single-Tool Call to Multi-Tool Orchestration
    "https://arxiv.org/abs/2603.22876",  # Grounding Sim-to-Real Generalization in Dexterous Manipulation: An Empirical Study with Vision-Language-Action Models
    "https://arxiv.org/abs/2603.22918",  # EVA: Efficient Reinforcement Learning for End-to-End Video Agent
    "https://arxiv.org/abs/2603.22953",  # Cluster-Wise Spatio-Temporal Masking for Efficient Video-Language Pretraining
    "https://arxiv.org/abs/2603.23355",  # Off-Policy Value-Based Reinforcement Learning for Large Language Models
    "https://arxiv.org/abs/2603.23376",  # ABot-PhysWorld: Interactive World Foundation Model for Robotic Manipulation with Physics Alignment
    "https://arxiv.org/abs/2603.23404",  # Unleashing Spatial Reasoning in Multimodal Large Language Models via Textual Representation Guided Reasoning
    "https://arxiv.org/abs/2603.23481",  # VTAM: Video-Tactile-Action Models for Complex Physical Interaction Beyond VLAs
    "https://arxiv.org/abs/2603.23483",  # SpecEyes: Accelerating Agentic Multimodal LLMs via Speculative Perception and Planning
    "https://arxiv.org/abs/2603.23497",  # WildWorld: A Large-Scale Dataset for Dynamic World Modeling with Actions and Explicit State toward Generative ARPG
    "https://arxiv.org/abs/2603.23500",  # UniGRPO: Unified Policy Optimization for Reasoning-Driven Visual Generation
    "https://arxiv.org/abs/2603.23889",  # Off-Policy Safe Reinforcement Learning with Constrained Optimistic Exploration
    "https://arxiv.org/abs/2603.24139",  # Tutor-Student Reinforcement Learning: A Dynamic Curriculum for Robust Deepfake Detection
    "https://arxiv.org/abs/2603.24322",  # Heuristic Self-Paced Learning for Domain Adaptive Semantic Segmentation under Adverse Conditions
    "https://arxiv.org/abs/2603.24350",  # Evidence of an Emergent \"Self\" in Continual Robot Learning
    "https://arxiv.org/abs/2603.24393",  # 3D-Mix for VLA: A Plug-and-Play Module for Integrating VGGT-based 3D Information into Vision-Language-Action Models
    "https://arxiv.org/abs/2603.24422",  # OneSearch-V2: The Latent Reasoning Enhanced Self-distillation Generative Search Framework
    "https://arxiv.org/abs/2603.24454",  # Unleashing Vision-Language Semantics for Deepfake Video Detection
    "https://arxiv.org/abs/2603.24506",  # Toward Physically Consistent Driving Video World Models under Challenging Trajectories
    "https://arxiv.org/abs/2603.24517",  # AVO: Agentic Variation Operators for Autonomous Evolutionary Search
    "https://arxiv.org/abs/2603.24533",  # UI-Voyager: A Self-Evolving GUI Agent Learning via Failed Experience
    "https://arxiv.org/abs/2603.24558",  # LensWalk: Agentic Video Understanding by Planning How You See in Videos
    "https://arxiv.org/abs/2603.24576",  # Chameleon: Episodic Memory for Long-Horizon Robotic Manipulation
    "https://arxiv.org/abs/2603.24581",  # Latent-WAM: Latent World Action Modeling for End-to-End Autonomous Driving
    "https://arxiv.org/abs/2603.24584",  # TAG: Target-Agnostic Guidance for Stable Object-Centric Inference in Vision-Language-Action Models
    "https://arxiv.org/abs/2603.24639",  # Experiential Reflective Learning for Self-Improving LLM Agents
    "https://arxiv.org/abs/2603.24800",  # Calibri: Enhancing Diffusion Transformers via Parameter-Efficient Calibration
    "https://arxiv.org/abs/2603.24866",  # How Far Are Vision-Language Models from Constructing the Real World? A Benchmark for Physical Generative Reasoning
    "https://arxiv.org/abs/2603.24984",  # MoE-GRPO: Optimizing Mixture-of-Experts via Reinforcement Learning in Vision-Language Models
    "https://arxiv.org/abs/2603.25038",  # $π$, But Make It Fly: Physics-Guided Transfer of VLA Models to Aerial Manipulation
    "https://arxiv.org/abs/2603.25040",  # Intern-S1-Pro: Scientific Multimodal Foundation Model at Trillion Scale
    "https://arxiv.org/abs/2603.25077",  # Bridging Perception and Reasoning: Token Reweighting for RLVR in Multimodal LLMs
    "https://arxiv.org/abs/2603.25108",  # MSRL: Scaling Generative Multimodal Reward Modeling via Multi-Stage Reinforcement Learning
    "https://arxiv.org/abs/2603.25111",  # SEVerA: Verified Synthesis of Self-Evolving Agents
    "https://arxiv.org/abs/2603.25118",  # AnyDoc: Enhancing Document Generation via Large-Scale HTML/CSS Data Synthesis and Height-Aware Reinforcement Optimization
    "https://arxiv.org/abs/2603.25188",  # AnyID: Ultra-Fidelity Universal Identity-Preserving Video Generation from Any Visual References
    "https://arxiv.org/abs/2603.25399",  # LaMP: Learning Vision-Language-Action Policies with 3D Scene Flow as Latent Motion Prior
    "https://arxiv.org/abs/2603.25406",  # MMaDA-VLA: Large Diffusion Vision-Language-Action Model with Unified Multi-Modal Instruction and Generation
    "https://arxiv.org/abs/2603.25411",  # HiSpatial: Taming Hierarchical 3D Spatial Understanding in Vision-Language Models
    "https://arxiv.org/abs/2603.25629",  # LanteRn: Latent Visual Structured Reasoning
    "https://arxiv.org/abs/2603.25681",  # Self-Improvement of Large Language Models: A Technical Overview and Future Outlook
    "https://arxiv.org/abs/2603.25685",  # Persistent Robot World Models: Stabilizing Multi-Step Rollouts via Reinforcement Learning
    "https://arxiv.org/abs/2603.25716",  # Out of Sight but Not Out of Mind: Hybrid Memory for Dynamic Video World Models
    "https://arxiv.org/abs/2603.25720",  # R-C2: Cycle-Consistent Reinforcement Learning Improves Multimodal Reasoning
    "https://arxiv.org/abs/2603.25723",  # Natural-Language Agent Harnesses
    "https://arxiv.org/abs/2603.25725",  # SoftMimicGen: A Data Generation System for Scalable Robot Learning in Deformable Object Manipulation
    "https://arxiv.org/abs/2603.25740",  # Drive My Way: Preference Alignment of Vision-Language-Action Model for Personalized Driving
    "https://arxiv.org/abs/2603.25744",  # MuRF: Unlocking the Multi-Scale Potential of Vision Foundation Models
    "https://arxiv.org/abs/2603.25887",  # World Reasoning Arena
    "https://arxiv.org/abs/2603.25902",  # Chasing Autonomy: Dynamic Retargeting and Control Guided RL for Performant and Controllable Humanoid Running
    "https://arxiv.org/abs/2603.25942",  # Reinforcing Structured Chain-of-Thought for Video Understanding
    "https://arxiv.org/abs/2603.25968",  # Neuro-Cognitive Reward Modeling for Human-Centered Autonomous Vehicle Control
    "https://arxiv.org/abs/2603.25981",  # Policy-Guided World Model Planning for Language-Conditioned Visual Navigation
    "https://arxiv.org/abs/2603.26164",  # DataFlex: A Unified Framework for Data-Centric Dynamic Training of Large Language Models
    "https://arxiv.org/abs/2603.26285",  # PhysVid: Physics Aware Local Conditioning for Generative Video Models
    "https://arxiv.org/abs/2603.26320",  # DFM-VLA: Iterative Action Refinement for Robot Manipulation via Discrete Flow Matching
    "https://arxiv.org/abs/2603.26499",  # AIRA_2: Overcoming Bottlenecks in AI Research Agents
    "https://arxiv.org/abs/2603.26599",  # VGGRPO: Towards World-Consistent Video Generation with 4D Latent Reward
    "https://arxiv.org/abs/2603.26666",  # VLA-OPD: Bridging Offline SFT and Online RL for Vision-Language-Action Models via On-Policy Distillation
    "https://arxiv.org/abs/2603.26799",  # Gaussian Joint Embeddings For Self-Supervised Representation Learning
    "https://arxiv.org/abs/2603.27164",  # daVinci-LLM:Towards the Science of Pretraining
    "https://arxiv.org/abs/2603.27179",  # Reasoning-Driven Anomaly Detection and Localization with Image-Level Supervision
    "https://arxiv.org/abs/2603.27287",  # Uni-World VLA: Interleaved World Modeling and Planning for Autonomous Driving
    "https://arxiv.org/abs/2603.27313",  # MetaTune: Adjoint-based Meta-tuning via Robotic Differentiable Dynamics
    "https://arxiv.org/abs/2603.27455",  # From None to All: Self-Supervised 3D Reconstruction via Novel View Synthesis
    "https://arxiv.org/abs/2603.27494",  # Learning to Focus and Precise Cropping: A Reinforcement Learning Framework with Information Gaps and Grounding Loss for MLLMs
    "https://arxiv.org/abs/2603.27670",  # ProgressVLA: Progress-Guided Diffusion Policy for Vision-Language Robotic Manipulation
    "https://arxiv.org/abs/2603.27866",  # Wan-R1: Verifiable-Reinforcement Learning for Video Reasoning
    "https://arxiv.org/abs/2603.27967",  # Learning Multi-View Spatial Reasoning from Cross-View Relations
    "https://arxiv.org/abs/2603.28116",  # $AutoDrive\text{-}P^3$: Unified Chain of Perception-Prediction-Planning Thought via Reinforcement Fine-Tuning
    "https://arxiv.org/abs/2603.28204",  # ERPO: Token-Level Entropy-Regulated Policy Optimization for Large Reasoning Models
    "https://arxiv.org/abs/2603.28301",  # LIBERO-Para: A Diagnostic Benchmark and Metrics for Paraphrase Robustness in VLA Models
    "https://arxiv.org/abs/2603.28386",  # COvolve: Adversarial Co-Evolution of Large-Language-Model-Generated Policies and Environments via Two-Player Zero-Sum Game
    "https://arxiv.org/abs/2603.28480",  # INSID3: Training-Free In-Context Segmentation with DINOv3
    "https://arxiv.org/abs/2603.28489",  # Video Generation Models as World Models: Efficient Paradigms, Architectures and Algorithms
    "https://arxiv.org/abs/2603.28545",  # ManipArena: Comprehensive Real-world Evaluation of Reasoning-Oriented Generalist Robot Manipulation
    "https://arxiv.org/abs/2603.28565",  # StreamingVLA: Streaming Vision-Language-Action Model with Action Flow Matching and Adaptive Early Observation
    "https://arxiv.org/abs/2603.28618",  # Seeing with You: Perception-Reasoning Coevolution for Multimodal Reasoning
    "https://arxiv.org/abs/2603.28713",  # DreamLite: A Lightweight On-Device Unified Model for Image Generation and Editing
    "https://arxiv.org/abs/2603.28718",  # Stepwise Credit Assignment for GRPO on Flow-Matching Models
    "https://arxiv.org/abs/2603.28730",  # SOLE-R1: Video-Language Reasoning as the Sole Reward for On-Robot Reinforcement Learning
    "https://arxiv.org/abs/2603.28740",  # FocusVLA: Focused Visual Utilization for Vision-Language-Action Models
    "https://arxiv.org/abs/2603.28887",  # OccSim: Multi-kilometer Simulation with Long-horizon Occupancy World Models
    "https://arxiv.org/abs/2603.28955",  # Enhancing Policy Learning with World-Action Model
    "https://arxiv.org/abs/2603.28963",  # AutoWorld: Scaling Multi-Agent Traffic Simulation with Self-Supervised World Models
    "https://arxiv.org/abs/2603.29089",  # WorldFlow3D: Flowing Through 3D Distributions for Unbounded World Generation
    "https://arxiv.org/abs/2603.29090",  # HCLSM: Hierarchical Causal Latent State Machines for Object-Centric World Modeling
    "https://arxiv.org/abs/2603.29165",  # LatentPilot: Scene-Aware Vision-and-Language Navigation by Dreaming Ahead with Latent Visual Reasoning
    "https://arxiv.org/abs/2603.29409",  # CLaD: Planning with Grounded Foresight via Cross-Modal Latent Dynamics
    "https://arxiv.org/abs/2603.29493",  # MemFactory: Unified Inference & Training Framework for Agent Memory
    "https://arxiv.org/abs/2603.29557",  # FlowPIE: Test-Time Scientific Idea Evolution with Flow-Guided Literature Exploration
    "https://arxiv.org/abs/2603.29620",  # Unify-Agent: A Unified Multimodal Agent for World-Grounded Image Synthesis
    "https://arxiv.org/abs/2603.29634",  # MacTok: Robust Continuous Tokenization for Image Generation
    "https://arxiv.org/abs/2603.29791",  # Reasoning-Driven Synthetic Data Generation and Evaluation
    "https://arxiv.org/abs/2603.29844",  # DIAL: Decoupling Intent and Action via Latent World Modeling for End-to-End VLA
    "https://arxiv.org/abs/2603.30022",  # Hybrid Framework for Robotic Manipulation: Integrating Reinforcement Learning and Large Language Models
    "https://arxiv.org/abs/2603.30036",  # Aligned, Orthogonal or In-conflict: When can we safely optimize Chain-of-Thought?
    "https://arxiv.org/abs/2603.30045",  # OmniRoam: World Wandering via Long-Horizon Panoramic Video Generation
    "https://arxiv.org/abs/2604.00061",  # Advancing Multi-Robot Networks via MLLM-Driven Sensing, Communication, and Computation: A Comprehensive Survey
    "https://arxiv.org/abs/2604.00202",  # DreamControl-v2: Simpler and Scalable Autonomous Humanoid Skills via Trainable Guided Diffusion Priors
    "https://arxiv.org/abs/2604.00479",  # All Roads Lead to Rome: Incentivizing Divergent Thinking in Vision-Language Models
    "https://arxiv.org/abs/2604.00530",  # AceTone: Bridging Words and Colors for Conditional Image Grading
    "https://arxiv.org/abs/2604.00626",  # A Survey of On-Policy Distillation for Large Language Models
    "https://arxiv.org/abs/2604.00849",  # Disentangling to Re-couple: Resolving the Similarity-Controllability Paradox in Subject-Driven Text-to-Image Generation
    "https://arxiv.org/abs/2604.00965",  # Understanding Transformers and Attention Mechanisms: An Introduction for Applied Mathematicians
    "https://arxiv.org/abs/2604.01001",  # EgoSim: Egocentric World Simulator for Embodied Interaction Generation
    "https://arxiv.org/abs/2604.01007",  # Omni-SimpleMem: Autoresearch-Guided Discovery of Lifelong Multimodal Agent Memory
    "https://arxiv.org/abs/2604.01158",  # SMASH: Mastering Scalable Whole-Body Skills for Humanoid Ping-Pong with Egocentric Vision
    "https://arxiv.org/abs/2604.01179",  # A ROS 2 Wrapper for Florence-2: Multi-Mode Local Vision-Language Inference for Robotic Systems
    "https://arxiv.org/abs/2604.01193",  # Embarrassingly Simple Self-Distillation Improves Code Generation
    "https://arxiv.org/abs/2604.01414",  # Learning When to See and When to Feel: Adaptive Vision-Torque Fusion for Contact-Aware Manipulation
    "https://arxiv.org/abs/2604.01421",  # EgoFlow: Gradient-Guided Flow Matching for Egocentric 6DoF Object Motion Generation
    "https://arxiv.org/abs/2604.01434",  # Leveraging the Value of Information in POMDP Planning
    "https://arxiv.org/abs/2604.01479",  # UniRecGen: Unifying Multi-View 3D Reconstruction and Generation
    "https://arxiv.org/abs/2604.01570",  # Boosting Vision-Language-Action Finetuning with Feasible Action Neighborhood Prior
    "https://arxiv.org/abs/2604.01600",  # MM-ReCoder: Advancing Chart-to-Code Generation with Reinforcement Learning and Self-Correction
    "https://arxiv.org/abs/2604.01618",  # Tex3D: Objects as Attack Surfaces via Adversarial 3D Textures for Vision-Language-Action Models
    "https://arxiv.org/abs/2604.01658",  # CORAL: Towards Autonomous Multi-Agent Evolution for Open-Ended Discovery
    "https://arxiv.org/abs/2604.01687",  # EvoSkills: Self-Evolving Agent Skills via Co-Evolutionary Verification
    "https://arxiv.org/abs/2604.01765",  # DriveDreamer-Policy: A Geometry-Grounded World-Action Model for Unified Generation and Planning
    "https://arxiv.org/abs/2604.01840",  # Not All Tokens See Equally: Perception-Grounded Policy Optimization for Large Vision-Language Models
    "https://arxiv.org/abs/2604.01913",  # The Rank and Gradient Lost in Non-stationarity: Sample Weight Decay for Mitigating Plasticity Loss in Reinforcement Learning
    "https://arxiv.org/abs/2604.01985",  # World Action Verifier: Self-Improving World Models via Forward-Inverse Asymmetry
    "https://arxiv.org/abs/2604.02021",  # Bridging Discrete Planning and Continuous Execution for Redundant Robot
    "https://arxiv.org/abs/2604.02029",  # The Latent Space: Foundation, Evolution, Mechanism, Ability, and Outlook
    "https://arxiv.org/abs/2604.02035",  # Reinforcement Learning for Speculative Trading under Exploratory Framework
    "https://arxiv.org/abs/2604.02073",  # PLUME: Latent Reasoning Based Universal Multimodal Embedding
    "https://arxiv.org/abs/2604.02097",  # LatentUM: Unleashing the Potential of Interleaved Cross-Modal Reasoning via a Latent-Space Unified Model
    "https://arxiv.org/abs/2604.02190",  # UniDriveVLA: Unifying Understanding, Perception, and Action Planning for Autonomous Driving
    "https://arxiv.org/abs/2604.02260",  # Model-Based Reinforcement Learning for Control under Time-Varying Dynamics
    "https://arxiv.org/abs/2604.02268",  # SKILL0: In-Context Agentic Reinforcement Learning for Skill Internalization
    "https://arxiv.org/abs/2604.02288",  # Unifying Group-Relative and Self-Distillation Policy Optimization via Sample Routing
    "https://arxiv.org/abs/2604.02296",  # VOID: Video Object and Interaction Deletion
    "https://arxiv.org/abs/2604.02317",  # A Simple Baseline for Streaming Video Understanding
    "https://arxiv.org/abs/2604.02327",  # Steerable Visual Representations
    "https://arxiv.org/abs/2604.02329",  # Generative World Renderer
    "https://arxiv.org/abs/2604.02349",  # OPRIDE: Offline Preference-based Reinforcement Learning via In-Dataset Exploration
    "https://arxiv.org/abs/2604.02355",  # From Broad Exploration to Stable Synthesis: Entropy-Guided Optimization for Autoregressive Image Generation
    "https://arxiv.org/abs/2604.02408",  # F2F-AP: Flow-to-Future Asynchronous Policy for Real-time Dynamic Manipulation
    "https://arxiv.org/abs/2604.02523",  # Tune to Learn: How Controller Gains Shape Robot Policy Learning
    "https://arxiv.org/abs/2604.02696",  # VBGS-SLAM: Variational Bayesian Gaussian Splatting Simultaneous Localization and Mapping
    "https://arxiv.org/abs/2604.02759",  # OMNI-PoseX: A Fast Vision Model for 6D Object Pose Estimation in Embodied Tasks
    "https://arxiv.org/abs/2604.02812",  # Learning Structured Robot Policies from Vision-Language Models via Synthetic Neuro-Symbolic Supervision
    "https://arxiv.org/abs/2604.02829",  # STRNet: Visual Navigation with Spatio-Temporal Representation through Dynamic Graph Aggregation
    "https://arxiv.org/abs/2604.02911",  # Learning Task-Invariant Properties via Dreamer: Enabling Efficient Policy Transfer for Quadruped Robots
    "https://arxiv.org/abs/2604.02965",  # Open-Loop Planning, Closed-Loop Verification: Speculative Verification for VLA
    "https://arxiv.org/abs/2604.03016",  # Agentic-MME: What Agentic Capability Really Brings to Multimodal Intelligence?
    "https://arxiv.org/abs/2604.03023",  # Behavior-Constrained Reinforcement Learning with Receding-Horizon Credit Assignment for High-Performance Control
    "https://arxiv.org/abs/2604.03037",  # ARM: Advantage Reward Modeling for Long-Horizon Manipulation
    "https://arxiv.org/abs/2604.03098",  # Co-Evolution of Policy and Internal Reward for Language Agents
    "https://arxiv.org/abs/2604.03128",  # Self-Distilled RLVR
    "https://arxiv.org/abs/2604.03179",  # Understanding the Role of Hallucination in Reinforcement Post-Training of Multimodal Reasoning Models
    "https://arxiv.org/abs/2604.03181",  # Multi-View Video Diffusion Policy: A 3D Spatio-Temporal-Aware Video Action Model
    "https://arxiv.org/abs/2604.03191",  # The Compression Gap: Why Discrete Tokenization Limits Vision-Language-Action Model Scaling
    "https://arxiv.org/abs/2604.03208",  # Hierarchical Planning with Latent World Models
    "https://arxiv.org/abs/2604.03489",  # Improving Feasibility via Fast Autoencoder-Based Projections
    "https://arxiv.org/abs/2604.03552",  # CRAFT: Video Diffusion for Bimanual Robot Data Generation
    "https://arxiv.org/abs/2604.03993",  # Can LLMs Learn to Reason Robustly under Noisy Supervision?
    "https://arxiv.org/abs/2604.04055",  # DINO-VO: Learning Where to Focus for Enhanced State Estimation
    "https://arxiv.org/abs/2604.04138",  # Learning Dexterous Grasping from Sparse Taxonomy Guidance
    "https://arxiv.org/abs/2604.04161",  # Adaptive Action Chunking at Inference-time for Vision-Language-Action Models
    "https://arxiv.org/abs/2604.04247",  # Combee: Scaling Prompt Learning for Self-Improving Language Model Agents
    "https://arxiv.org/abs/2604.04310",  # frax: Fast Robot Kinematics and Dynamics in JAX
    "https://arxiv.org/abs/2604.04379",  # Reinforce to Learn, Elect to Reason: A Dual Paradigm for Video Reasoning
    "https://arxiv.org/abs/2604.04502",  # Veo-Act: How Far Can Frontier Video Models Advance Generalizable Robot Manipulation?
    "https://arxiv.org/abs/2604.04503",  # Memory Intelligence Agent
    "https://arxiv.org/abs/2604.04539",  # FlashSAC: Fast and Stable Off-Policy Reinforcement Learning for High-Dimensional Robot Control
    "https://arxiv.org/abs/2604.04646",  # Training-Free Refinement of Flow Matching with Divergence-based Sampling
    "https://arxiv.org/abs/2604.04648",  # From Curiosity to Caution: Mitigating Reward Hacking for Best-of-N with Pessimism
    "https://arxiv.org/abs/2604.04664",  # ROSClaw: A Hierarchical Semantic-Physical Framework for Heterogeneous Multi-Agent Collaboration
    "https://arxiv.org/abs/2604.04707",  # OpenWorldLib: A Unified Codebase and Definition of Advanced World Models
    "https://arxiv.org/abs/2604.04746",  # Think in Strokes, Not Pixels: Process-Driven Image Generation via Interleaved Reasoning
    "https://arxiv.org/abs/2604.04872",  # Synthetic Sandbox for Training Machine Learning Engineering Agents
    "https://arxiv.org/abs/2604.04911",  # SpatialEdit: Benchmarking Fine-Grained Image Spatial Editing
    "https://arxiv.org/abs/2604.04913",  # A Frame is Worth One Token: Efficient Generative World Modeling with Delta Tokens
    "https://arxiv.org/abs/2604.04917",  # Vero: An Open RL Recipe for General Visual Reasoning
    "https://arxiv.org/abs/2604.04974",  # From Video to Control: A Survey of Learning Manipulation Interfaces from Temporal Visual Data
    "https://arxiv.org/abs/2604.05014",  # StarVLA: A Lego-like Codebase for Vision-Language-Action Model Developing
    "https://arxiv.org/abs/2604.05091",  # MegaTrain: Full Precision Training of 100B+ Parameter Large Language Models on a Single GPU
    "https://arxiv.org/abs/2604.05112",  # Vintix II: Decision Pre-Trained Transformer is a Scalable In-Context Reinforcement Learner
    "https://arxiv.org/abs/2604.05323",  # VLA-InfoEntropy: A Training-Free Vision-Attention Information Entropy Approach for Vision-Language-Action Models Inference Acceleration and Success
    "https://arxiv.org/abs/2604.05355",  # ETR: Entropy Trend Reward for Efficient Chain-of-Thought Reasoning
    "https://arxiv.org/abs/2604.05484",  # CoEnv: Driving Embodied Multi-Agent Collaboration via Compositional Environment
    "https://arxiv.org/abs/2604.05498",  # JailWAM: Jailbreaking World Action Models in Robot Control
    "https://arxiv.org/abs/2604.05595",  # Uncovering Linguistic Fragility in Vision-Language-Action Models via Diversity-Aware Red Teaming
    "https://arxiv.org/abs/2604.05614",  # Grounding Hierarchical Vision-Language-Action Models Through Explicit Language-Action Alignment
    "https://arxiv.org/abs/2604.05621",  # FunRec: Reconstructing Functional 3D Scenes from Egocentric Interaction Videos
    "https://arxiv.org/abs/2604.05656",  # SnapFlow: One-Step Action Generation for Flow-Matching VLAs via Progressive Self-Distillation
    "https://arxiv.org/abs/2604.05672",  # A1: A Fully Transparent Open-Source, Adaptive and Efficient Truncated Vision-Language-Action Model
    "https://arxiv.org/abs/2604.05831",  # BiCoord: A Bimanual Manipulation Benchmark towards Long-Horizon Spatial-Temporal Coordination
    "https://arxiv.org/abs/2604.05931",  # Saliency-Guided Representation with Consistency Policy Learning for Visual Unsupervised Reinforcement Learning
    "https://arxiv.org/abs/2604.06067",  # HiPolicy: Hierarchical Multi-Frequency Action Chunking for Policy Learning
    "https://arxiv.org/abs/2604.06126",  # Gym-Anything: Turn any Software into an Agent Environment
    "https://arxiv.org/abs/2604.06168",  # Action Images: End-to-End Policy Learning via Multiview Video Generation
    "https://arxiv.org/abs/2604.06169",  # In-Place Test-Time Training
    "https://arxiv.org/abs/2604.06268",  # RAGEN-2: Reasoning Collapse in Agentic RL
    "https://arxiv.org/abs/2604.06628",  # Rethinking Generalization in Reasoning SFT: A Conditional Analysis on Optimization, Data, and Model Capability
    "https://arxiv.org/abs/2604.06778",  # RichMap: A Reachability Map Balancing Precision, Efficiency, and Flexibility for Rich Robot Manipulation Tasks
    "https://arxiv.org/abs/2604.06870",  # RefineAnything: Multimodal Region-Specific Refinement for Perfect Local Details
    "https://arxiv.org/abs/2604.06943",  # Sustainable Transfer Learning for Adaptive Robot Skills
    "https://arxiv.org/abs/2604.07084",  # Flow Motion Policy: Manipulator Motion Planning with Flow Matching Models
    "https://arxiv.org/abs/2604.07105",  # Genie Sim PanoRecon: Fast Immersive Scene Generation from Single-View Panorama
    "https://arxiv.org/abs/2604.07209",  # INSPATIO-WORLD: A Real-Time 4D World Simulator via Spatiotemporal Autoregressive Modeling
    "https://arxiv.org/abs/2604.07335",  # TAMEn: Tactile-Aware Manipulation Engine for Closed-Loop Data Collection in Contact-Rich Tasks
    "https://arxiv.org/abs/2604.07348",  # MoRight: Motion Control Done Right
    "https://arxiv.org/abs/2604.07392",  # Event-Centric World Modeling with Memory-Augmented Retrieval for Embodied Decision-Making
    "https://arxiv.org/abs/2604.07430",  # HY-Embodied-0.5: Embodied Foundation Models for Real-World Agents
    "https://arxiv.org/abs/2604.07457",  # CMP: Robust Whole-Body Tracking for Loco-Manipulation via Competence Manifold Projection
    "https://arxiv.org/abs/2604.07480",  # Active Reward Machine Inference From Raw State Trajectories
    "https://arxiv.org/abs/2604.07592",  # Spatio-Temporal Grounding of Large Language Models from Perception Streams
    "https://arxiv.org/abs/2604.07607",  # EgoVerse: An Egocentric Human Dataset for Robot Learning from Around the World
    "https://arxiv.org/abs/2604.07725",  # Squeeze Evolve: Unified Multi-Model Orchestration for Verifier-Free Evolution
    "https://arxiv.org/abs/2604.07774",  # RoboAgent: Chaining Basic Capabilities for Embodied Task Planning
    "https://arxiv.org/abs/2604.07799",  # Learning Without Losing Identity: Capability Evolution for Embodied Agents
    "https://arxiv.org/abs/2604.07822",  # Loop, Think, & Generalize: Implicit Reasoning in Recurrent-Depth Transformers
    "https://arxiv.org/abs/2604.07882",  # ReconPhys: Reconstruct Appearance and Physical Attributes from Single Video
    "https://arxiv.org/abs/2604.07957",  # WorldMAP: Bootstrapping Vision-Language Navigation Trajectory Prediction with Generative World Models
    "https://arxiv.org/abs/2604.07993",  # HEX: Humanoid-Aligned Experts for Cross-Embodiment Whole-Body Manipulation
    "https://arxiv.org/abs/2604.08121",  # Uni-ViGU: Towards Unified Video Generation and Understanding via A Diffusion-Based Video Generator
    "https://arxiv.org/abs/2604.08168",  # ViVa: A Video-Generative Value Model for Robot Reinforcement Learning
    "https://arxiv.org/abs/2604.08258",  # EvoGymCM: Harnessing Continuous Material Stiffness for Soft Robot Co-Design
    "https://arxiv.org/abs/2604.08418",  # Exploring Temporal Representation in Neural Processes for Multimodal Action Prediction
    "https://arxiv.org/abs/2604.08509",  # Visually-grounded Humanoid Agents
    "https://arxiv.org/abs/2604.08532",  # Self-Improving 4D Perception via Self-Distillation
    "https://arxiv.org/abs/2604.08534",  # ActiveGlasses: Learning Manipulation with Active Vision from Ego-centric Human Demonstration
    "https://arxiv.org/abs/2604.08539",  # OpenVLThinkerV2: A Generalist Multimodal Reasoning Model for Multi-domain Visual Tasks
    "https://arxiv.org/abs/2604.08544",  # SIM1: Physics-Aligned Simulator as Zero-Shot Data Scaler in Deformable Worlds
    "https://arxiv.org/abs/2604.08545",  # Act Wisely: Cultivating Meta-Cognitive Tool Use in Agentic Multimodal Models
    "https://arxiv.org/abs/2604.08626",  # WildDet3D: Scaling Promptable 3D Detection in the Wild
    "https://arxiv.org/abs/2604.08706",  # Efficient RL Training for LLMs with Experience Replay
    "https://arxiv.org/abs/2604.08780",  # Toward Hardware-Agnostic Quadrupedal World Models via Morphology Conditioning
    "https://arxiv.org/abs/2604.08865",  # SPPO: Sequence-Level PPO for Long-Horizon Reasoning Tasks
    "https://arxiv.org/abs/2604.08883",  # HTNav: A Hybrid Navigation Framework with Tiered Structure for Urban Aerial Vision-and-Language Navigation
    "https://arxiv.org/abs/2604.08958",  # WOMBET: World Model-based Experience Transfer for Robust and Sample-efficient Reinforcement Learning
    "https://arxiv.org/abs/2604.08995",  # Matrix-Game 3.0: Real-Time and Streaming Interactive World Model with Long-Horizon Memory
    "https://arxiv.org/abs/2604.09059",  # Learning Vision-Language-Action World Models for Autonomous Driving
    "https://arxiv.org/abs/2604.09168",  # ELT: Elastic Looped Transformers for Visual Generation
    "https://arxiv.org/abs/2604.09258",  # Nexus: Same Pretraining Loss, Better Downstream Generalization via Common Minima
    "https://arxiv.org/abs/2604.09294",  # A Benchmark of Dexterity for Anthropomorphic Robotic Hands
    "https://arxiv.org/abs/2604.09330",  # VAG: Dual-Stream Video-Action Generation for Embodied Data Synthesis
    "https://arxiv.org/abs/2604.09415",  # PhysInOne: Visual Physics Learning and Reasoning in One Suite
    "https://arxiv.org/abs/2604.09445",  # AsymLoc: Towards Asymmetric Feature Matching for Efficient Visual Localization
    "https://arxiv.org/abs/2604.09452",  # SafeAdapt: Provably Safe Policy Updates in Deep Reinforcement Learning
    "https://arxiv.org/abs/2604.09651",  # FlowHijack: A Dynamics-Aware Backdoor Attack on Flow-Matching Vision-Language-Action Models
    "https://arxiv.org/abs/2604.09860",  # RoboLab: A High-Fidelity Simulation Benchmark for Analysis of Task Generalist Policies
    "https://arxiv.org/abs/2604.10096",  # ABot-Claw: A Foundation for Persistent, Cooperative, and Self-Evolving Robotic Agents
    "https://arxiv.org/abs/2604.10165",  # MoRI: Mixture of RL and IL Experts for Long-Horizon Manipulation Tasks
    "https://arxiv.org/abs/2604.10333",  # Zero-shot World Models Are Developmentally Efficient Learners
    "https://arxiv.org/abs/2604.10579",  # AffordGen: Generating Diverse Demonstrations for Generalizable Object Manipulation with Afford Correspondence
    "https://arxiv.org/abs/2604.10677",  # LIDEA: Human-to-Robot Imitation Learning via Implicit Feature Distillation and Explicit Geometry Alignment
    "https://arxiv.org/abs/2604.10836",  # HO-Flow: Generalizable Hand-Object Interaction Generation with Latent Flow Matching
    "https://arxiv.org/abs/2604.10856",  # BridgeSim: Unveiling the OL-CL Gap in End-to-End Autonomous Driving
    "https://arxiv.org/abs/2604.10892",  # HECTOR: Human-centric Hierarchical Coordination and Supervision of Robotic Fleets under Continual Temporal Tasks
    "https://arxiv.org/abs/2604.10929",  # Ro-SLM: Onboard Small Language Models for Robot Task Planning and Operation Code Generation
    "https://arxiv.org/abs/2604.10949",  # Pseudo-Unification: Entropy Probing Reveals Divergent Information Patterns in Unified Multimodal Models
    "https://arxiv.org/abs/2604.10953",  # Diffusion Reinforcement Learning Based Online 3D Bin Packing Spatial Strategy Optimization
    "https://arxiv.org/abs/2604.10962",  # ScoRe-Flow: Complete Distributional Control via Score-Based Reinforcement Learning for Flow Matching
    "https://arxiv.org/abs/2604.10971",  # MMR-AD: A Large-Scale Multimodal Dataset for Benchmarking General Anomaly Detection with Multimodal Large Language Models
    "https://arxiv.org/abs/2604.10982",  # Ψ-Map: Panoptic Surface Integrated Mapping Enables Real2Sim Transfer
    "https://arxiv.org/abs/2604.11090",  # Simulator Adaptation for Sim-to-Real Learning of Legged Locomotion via Proprioceptive Distribution Matching
    "https://arxiv.org/abs/2604.11135",  # AIM: Intent-Aware Unified world action Modeling with Spatial Value Maps
    "https://arxiv.org/abs/2604.11138",  # ViserDex: Visual Sim-to-Real for Robust Dexterous In-hand Reorientation
    "https://arxiv.org/abs/2604.11201",  # CocoaBench: Evaluating Unified Digital Agents in the Wild
    "https://arxiv.org/abs/2604.11251",  # CLAW: Composable Language-Annotated Whole-body Motion Generation
    "https://arxiv.org/abs/2604.11297",  # The Past Is Not Past: Memory-Enhanced Dynamic Reward Shaping
    "https://arxiv.org/abs/2604.11302",  # 3D-Anchored Lookahead Planning for Persistent Robotic Scene Memory via World-Model-Based MCTS
    "https://arxiv.org/abs/2604.11306",  # Learning to Forget -- Hierarchical Episodic Memory for Lifelong Robot Deployment
    "https://arxiv.org/abs/2604.11320",  # CLASP: Closed-loop Asynchronous Spatial Perception for Open-vocabulary Desktop Object Grasping
    "https://arxiv.org/abs/2604.11351",  # WM-DAgger: Enabling Efficient Data Aggregation for Imitation Learning with World Models
    "https://arxiv.org/abs/2604.11373",  # Minimal Embodiment Enables Efficient Learning of Number Concepts in Robot
    "https://arxiv.org/abs/2604.11386",  # ComSim: Building Scalable Real-World Robot Data Generation via Compositional Simulation
    "https://arxiv.org/abs/2604.11626",  # RationalRewards: Reasoning Rewards Scale Visual Generation Both Training and Test Time
    "https://arxiv.org/abs/2604.11674",  # AffordSim: A Scalable Data Generator and Benchmark for Affordance-Aware Robotic Manipulation
    "https://arxiv.org/abs/2604.11689",  # LARY: A Latent Action Representation Yielding Benchmark for Generalizable Vision-to-Action Alignment
    "https://arxiv.org/abs/2604.11734",  # Multi-ORFT: Stable Online Reinforcement Fine-Tuning for Multi-Agent Diffusion Planning in Cooperative Driving
    "https://arxiv.org/abs/2604.11751",  # Grounded World Model for Semantically Generalizable Planning
    "https://arxiv.org/abs/2604.11757",  # StarVLA-$α$: Reducing Complexity in Vision-Language-Action Systems
    "https://arxiv.org/abs/2604.11768",  # Identifying Inductive Biases for Robot Co-Design
    "https://arxiv.org/abs/2604.11791",  # A Mechanistic Analysis of Looped Reasoning Language Models
    "https://arxiv.org/abs/2604.11805",  # Solving Physics Olympiad via Reinforcement Learning on Physics Simulators
    "https://arxiv.org/abs/2604.11992",  # ReefMapGS: Enabling Large-Scale Underwater Reconstruction by Closing the Loop Between Multimodal SLAM and Gaussian Splatting
    "https://arxiv.org/abs/2604.12002",  # Self-Distillation Zero: Self-Revision Turns Binary Rewards into Dense Supervision
    "https://arxiv.org/abs/2604.12012",  # TIPSv2: Advancing Vision-Language Pretraining with Enhanced Patch-Text Alignment
    "https://arxiv.org/abs/2604.12086",  # Robust Optimization for Mitigating Reward Hacking with Correlated Proxies
    "https://arxiv.org/abs/2604.12148",  # ViLL-E: Video LLM Embeddings for Retrieval
    "https://arxiv.org/abs/2604.12837",  # GGD-SLAM: Monocular 3DGS SLAM Powered by Generalizable Motion Model for Dynamic Environments
    "https://arxiv.org/abs/2604.12908",  # Robotic Manipulation is Vision-to-Geometry Mapping ($f(v) \rightarrow G$): Vision-Geometry Backbones over Language and Video Models
    "https://arxiv.org/abs/2604.12942",  # RMGS-SLAM: Real-time Multi-sensor Gaussian Splatting SLAM
    "https://arxiv.org/abs/2604.13010",  # Lightning OPD: Efficient Post-Training for Large Reasoning Models with Offline On-Policy Distillation
    "https://arxiv.org/abs/2604.13015",  # Learning Versatile Humanoid Manipulation with Touch Dreaming
    "https://arxiv.org/abs/2604.13016",  # Rethinking On-Policy Distillation of Large Language Models: Phenomenology, Mechanism, and Recipe
    "https://arxiv.org/abs/2604.13036",  # Lyra 2.0: Explorable Generative 3D Worlds
    "https://arxiv.org/abs/2604.13074",  # PersonaVLM: Long-Term Personalized Multimodal LLMs
    "https://arxiv.org/abs/2604.13596",  # VGGT-Segmentor: Geometry-Enhanced Cross-View Segmentation
    "https://arxiv.org/abs/2604.13788",  # Failure Identification in Imitation Learning Via Statistical and Semantic Filtering
    "https://arxiv.org/abs/2604.14084",  # TIP: Token Importance in On-Policy Distillation
    "https://arxiv.org/abs/2604.14089",  # UMI-3D: Extending Universal Manipulation Interface from Vision-Limited to 3D Spatial Perception
    "https://arxiv.org/abs/2604.14125",  # HiVLA: A Visual-Grounded-Centric Hierarchical Embodied Manipulation System
    "https://arxiv.org/abs/2604.14141",  # Geometric Context Transformer for Streaming 3D Reconstruction
    "https://arxiv.org/abs/2604.14144",  # SpatialEvo: Self-Evolving Spatial Intelligence via Deterministic Geometric Environments
    "https://arxiv.org/abs/2604.14258",  # GFT: From Imitation to Reward Fine-Tuning with Unbiased Group Advantages and Dynamic Coefficient Rectification
    "https://arxiv.org/abs/2604.14265",  # Reinforcement Learning via Value Gradient Flow
    "https://arxiv.org/abs/2604.14268",  # HY-World 2.0: A Multi-Modal World Model for Reconstructing, Generating, and Simulating 3D Worlds
    "https://arxiv.org/abs/2604.14732",  # World-Value-Action Model: Implicit Planning for Vision-Language-Action Systems
    "https://arxiv.org/abs/2604.15034",  # Autogenesis: A Self-Evolving Agent Protocol
    "https://arxiv.org/abs/2604.15215",  # A Hierarchical Spatiotemporal Action Tokenizer for In-Context Imitation Learning in Robotics
    "https://arxiv.org/abs/2604.15281",  # R3D: Revisiting 3D Policy Learning
    "https://arxiv.org/abs/2604.15306",  # Generalization in LLM Problem Solving: The Case of the Shortest Path
    "https://arxiv.org/abs/2604.15311",  # LeapAlign: Post-Training Flow Matching Models at Any Generation Step by Building Two-Step Trajectories
    "https://arxiv.org/abs/2604.15395",  # Foundation Models in Robotics: A Comprehensive Review of Methods, Models, Datasets, Challenges and Future Research Directions
    "https://arxiv.org/abs/2604.15475",  # NeuroMesh: A Unified Neural Inference Framework for Decentralized Multi-Robot Collaboration
    "https://arxiv.org/abs/2604.15483",  # $π_{0.7}$: a Steerable Generalist Robotic Foundation Model with Emergent Capabilities
    "https://arxiv.org/abs/2604.15574",  # Why Fine-Tuning Encourages Hallucinations and How to Fix It
    "https://arxiv.org/abs/2604.15805",  # From Seeing to Simulating: Generative High-Fidelity Simulation with Digital Cousins for Generalizable Robot Learning and Evaluation
    "https://arxiv.org/abs/2604.15809",  # Aligning What Vision-Language Models See and Perceive with Adaptive Information Flow
    "https://arxiv.org/abs/2604.15814",  # Continual Hand-Eye Calibration for Open-world Robotic Manipulation
    "https://arxiv.org/abs/2604.15911",  # Efficient Video Diffusion Models: Advancements and Challenges
    "https://arxiv.org/abs/2604.15938",  # VADF: Vision-Adaptive Diffusion Policy Framework for Efficient Robotic Manipulation
    "https://arxiv.org/abs/2604.16004",  # AgentV-RL: Scaling Reward Modeling with Agentic Verifier
    "https://arxiv.org/abs/2604.16027",  # Where does output diversity collapse in post-training?
    "https://arxiv.org/abs/2604.16029",  # Cut Your Losses! Learning to Prune Paths Early for Efficient Parallel Reasoning
    "https://arxiv.org/abs/2604.16044",  # Elucidating the SNR-t Bias of Diffusion Probabilistic Models
    "https://arxiv.org/abs/2604.16391",  # Disentangled Robot Learning via Separate Forward and Inverse Dynamics Pretraining
    "https://arxiv.org/abs/2604.16484",  # DexWorldModel: Causal Latent World Modeling towards Automated Learning of Embodied Tasks
    "https://arxiv.org/abs/2604.16592",  # Human Cognition in Machines: A Unified Perspective of World Models
    "https://arxiv.org/abs/2604.16677",  # ReconVLA: An Uncertainty-Guided and Failure-Aware Vision-Language-Action Framework for Robotic Control
    "https://arxiv.org/abs/2604.16893",  # EasyVideoR1: Easier RL for Video Understanding
    "https://arxiv.org/abs/2604.17245",  # MM-Hand: A 21-DOF Multi-modal Modular Dexterous Robotic Hand with Remote Actuation
    "https://arxiv.org/abs/2604.17335",  # Learning Whole-Body Humanoid Locomotion via Motion Generation and Motion Tracking
    "https://arxiv.org/abs/2604.17535",  # OPSDL: On-Policy Self-Distillation for Long-Context Language Models
    "https://arxiv.org/abs/2604.17651",  # Infrastructure-Centric World Models: Bridging Temporal Depth and Spatial Breadth for Roadside Perception
    "https://arxiv.org/abs/2604.17654",  # Poly-EPO: Training Exploratory Reasoning Models
    "https://arxiv.org/abs/2604.17706",  # OmniVLA-RL: A Vision-Language-Action Model with Spatial Understanding and Online RL
    "https://arxiv.org/abs/2604.17800",  # ReFineVLA: Multimodal Reasoning-Aware Generalist Robotic Policies via Teacher-Guided Fine-Tuning
    "https://arxiv.org/abs/2604.17807",  # Re$^2$MoGen: Open-Vocabulary Motion Generation via LLM Reasoning and Physics-Aware Refinement
    "https://arxiv.org/abs/2604.17876",  # OFlow: Injecting Object-Aware Temporal Flow Matching for Robust Robotic Manipulation
    "https://arxiv.org/abs/2604.17880",  # ST-$π$: Structured SpatioTemporal VLA for Robotic Manipulation
    "https://arxiv.org/abs/2604.17887",  # StableIDM: Stabilizing Inverse Dynamics Model against Manipulator Truncation via Spatio-Temporal Refinement
    "https://arxiv.org/abs/2604.17896",  # Can Explicit Physical Feasibility Benefit VLA Learning? An Empirical Study
    "https://arxiv.org/abs/2604.18075",  # Enhancing Continual Learning of Vision-Language Models via Dynamic Prefix Weighting
    "https://arxiv.org/abs/2604.18107",  # Test-Time Perturbation Learning with Delayed Feedback for Vision-Language-Action Models
    "https://arxiv.org/abs/2604.18131",  # Training LLM Agents for Spontaneous, Reward-Free Self-Evolution via World Knowledge Exploration
    "https://arxiv.org/abs/2604.18161",  # Does "Do Differentiable Simulators Give Better Policy Gradients?'' Give Better Policy Gradients?
    "https://arxiv.org/abs/2604.18267",  # MARCO: Navigating the Unseen Space of Semantic Correspondence
    "https://arxiv.org/abs/2604.18292",  # Agent-World: Scaling Real-World Environment Synthesis for Evolving General Agent Intelligence
    "https://arxiv.org/abs/2604.18484",  # XEmbodied: A Foundation Model with Enhanced Geometric and Physical Cues for Large-Scale Embodied Environments
    "https://arxiv.org/abs/2604.18486",  # OneVL: One-Step Latent Reasoning and Planning with Vision-Language Explanation
    "https://arxiv.org/abs/2604.18557",  # SynAgent: Generalizable Cooperative Humanoid Manipulation via Solo-to-Cooperative Agent Synergy
    "https://arxiv.org/abs/2604.18564",  # MultiWorld: Scalable Multi-Agent Multi-View Video World Models
    "https://arxiv.org/abs/2604.18791",  # HELM: Harness-Enhanced Long-horizon Memory for Vision-Language-Action Manipulation
    "https://arxiv.org/abs/2604.18811",  # Rethinking Dataset Distillation: Hard Truths about Soft Labels
    "https://arxiv.org/abs/2604.18867",  # Hierarchically Robust Zero-shot Vision-language Models
    "https://arxiv.org/abs/2604.18933",  # Gated Memory Policy
    "https://arxiv.org/abs/2604.18978",  # Low-Rank Adaptation for Critic Learning in Off-Policy Reinforcement Learning
    "https://arxiv.org/abs/2604.19092",  # RoboWM-Bench: A Benchmark for Evaluating World Models in Robotic Manipulation
    "https://arxiv.org/abs/2604.19254",  # ShadowPEFT: Shadow Network for Parameter-Efficient Fine-Tuning
    "https://arxiv.org/abs/2604.19406",  # HP-Edit: A Human-Preference Post-Training Framework for Image Editing
    "https://arxiv.org/abs/2604.19677",  # Learning Hybrid-Control Policies for High-Precision In-Contact Manipulation Under Uncertainty
    "https://arxiv.org/abs/2604.19683",  # Mask World Model: Predicting What Matters for Robust Robot Policy Learning
    "https://arxiv.org/abs/2604.19728",  # VLA Foundry: A Unified Framework for Training Vision-Language-Action Models
    "https://arxiv.org/abs/2604.19730",  # FASTER: Value-Guided Sampling for Fast RL
    "https://arxiv.org/abs/2604.19734",  # UniT: Toward a Unified Physical Language for Human-to-Humanoid Policy Learning and World Modeling
    "https://arxiv.org/abs/2604.19737",  # Safe Continual Reinforcement Learning in Non-stationary Environments
    "https://arxiv.org/abs/2604.19747",  # AnyRecon: Arbitrary-View 3D Reconstruction with Video Diffusion Model
    "https://arxiv.org/abs/2604.19839",  # Environmental Understanding Vision-Language Model for Embodied Agent
    "https://arxiv.org/abs/2604.20012",  # EmbodiedMidtrain: Bridging the Gap between Vision-Language Models and Vision-Language-Action Models via Mid-training
    "https://arxiv.org/abs/2604.20100",  # JoyAI-RA 0.1: A Foundation Model for Robotic Autonomy
    "https://arxiv.org/abs/2604.20209",  # Scaling Self-Play with Self-Guidance
    "https://arxiv.org/abs/2604.20328",  # Hybrid Latent Reasoning with Decoupled Policy Optimization
    "https://arxiv.org/abs/2604.20366",  # Mitigating Hallucinations in Large Vision-Language Models without Performance Degradation
    "https://arxiv.org/abs/2604.20444",  # VTouch++: A Multimodal Dataset with Vision-Based Tactile Enhancement for Bimanual Manipulation
    "https://arxiv.org/abs/2604.20472",  # Temporal Difference Calibration in Sequential Tasks: Application to Vision-Language-Action Models
    "https://arxiv.org/abs/2604.20473",  # Video-ToC: Video Tree-of-Cue Reasoning
    "https://arxiv.org/abs/2604.20570",  # Exploring Spatial Intelligence from a Generative Perspective
    "https://arxiv.org/abs/2604.20627",  # Occupancy Reward Shaping: Improving Credit Assignment for Offline Goal-Conditioned Reinforcement Learning
    "https://arxiv.org/abs/2604.20689",  # FingerEye: Continuous and Unified Vision-Tactile Sensing for Dexterous Manipulation
    "https://arxiv.org/abs/2604.20705",  # SSL-R1: Self-Supervised Visual Reinforcement Post-Training for Multimodal Large Language Models
    "https://arxiv.org/abs/2604.20733",  # Near-Future Policy Optimization
    "https://arxiv.org/abs/2604.20834",  # PokeVLA: Empowering Pocket-Sized Vision-Language-Action Model with Comprehensive World Knowledge Guidance
    "https://arxiv.org/abs/2604.20841",  # DeVI: Physics-based Dexterous Human-Object Interaction via Synthetic Video Imitation
    "https://arxiv.org/abs/2604.20987",  # Co-Evolving LLM Decision and Skill Bank Agents for Long-Horizon Tasks
    "https://arxiv.org/abs/2604.21192",  # How VLAs (Really) Work In Open-World Environments
    "https://arxiv.org/abs/2604.21232",  # ReCAPA: Hierarchical Predictive Correction to Mitigate Cascading Failures
    "https://arxiv.org/abs/2604.21254",  # Hyperloop Transformers
    "https://arxiv.org/abs/2604.21343",  # Latent Denoising Improves Visual Alignment in Large Multimodal Models
    "https://arxiv.org/abs/2604.21396",  # VG-CoT: Towards Trustworthy Visual Reasoning via Grounded Chain-of-Thought
    "https://arxiv.org/abs/2604.21409",  # S1-VL: Scientific Multimodal Reasoning Model with Thinking-with-Images
    "https://arxiv.org/abs/2604.21568",  # A Bayesian Reasoning Framework for Robotic Systems in Autonomous Casualty Triage
    "https://arxiv.org/abs/2604.21686",  # WorldMark: A Unified Benchmark Suite for Interactive Video World Models
    "https://arxiv.org/abs/2604.21741",  # Hi-WM: Human-in-the-World-Model for Scalable Robot Post-Training
    "https://arxiv.org/abs/2604.21764",  # Thinking with Reasoning Skills: Fewer Tokens, More Accuracy
    "https://arxiv.org/abs/2604.21873",  # Grounding Video Reasoning in Physical Signals
    "https://arxiv.org/abs/2604.21914",  # VistaBot: View-Robust Robot Manipulation via Spatiotemporal-Aware View Synthesis
    "https://arxiv.org/abs/2604.21924",  # Long-Horizon Manipulation via Trace-Conditioned VLA Planning
    "https://arxiv.org/abs/2604.22074",  # Outcome Rewards Do Not Guarantee Verifiable or Causally Important Reasoning
    "https://arxiv.org/abs/2604.22152",  # dWorldEval: Scalable Robotic Policy Evaluation via Discrete Diffusion World Model
    "https://arxiv.org/abs/2604.22446",  # From Skills to Talent: Organising Heterogeneous Agents as a Real-World Company
    "https://arxiv.org/abs/2604.22591",  # RedVLA: Physical Red Teaming for Vision-Language-Action Models
    "https://arxiv.org/abs/2604.22615",  # GazeVLA: Learning Human Intention for Robotic Manipulation
    "https://arxiv.org/abs/2604.22709",  # Thinking Without Words: Efficient Latent Reasoning with Abstract Chain-of-Thought
    "https://arxiv.org/abs/2604.22748",  # Agentic World Modeling: Foundations, Capabilities, Laws, and Beyond
    "https://arxiv.org/abs/2604.22875",  # SketchVLM: Vision language models can annotate images to explain thoughts and guide users
    "https://arxiv.org/abs/2604.22884",  # Can Multimodal Large Language Models Truly Understand Small Objects?
    "https://arxiv.org/abs/2604.23073",  # RL Token: Bootstrapping Online RL with Vision-Language-Action Models
    "https://arxiv.org/abs/2604.23121",  # Breaking Lock-In: Preserving Steerability under Low-Data VLA Post-Training
    "https://arxiv.org/abs/2604.23380",  # V-GRPO: Online Reinforcement Learning for Denoising Generative Models Is Easier than You Think
    "https://arxiv.org/abs/2604.23626",  # GraphPlanner: Graph Memory-Augmented Agentic Routing for Multi-Agent LLMs
    "https://arxiv.org/abs/2604.23702",  # QuietWalk: Physics-Informed Reinforcement Learning for Ground Reaction Force-Aware Humanoid Locomotion Under Diverse Footwear
    "https://arxiv.org/abs/2604.23747",  # SFT-then-RL Outperforms Mixed-Policy Methods for LLM Reasoning
    "https://arxiv.org/abs/2604.23775",  # Vision-Language-Action Safety: Threats, Challenges, Evaluations, and Mechanisms
    "https://arxiv.org/abs/2604.24018",  # Betting for Sim-to-Real Performance Evaluation
    "https://arxiv.org/abs/2604.24171",  # POCA: Pareto-Optimal Curriculum Alignment for Visual Text Generation
    "https://arxiv.org/abs/2604.24182",  # $M^2$-VLA: Boosting Vision-Language Models for Generalizable Manipulation via Layer Mixture and Meta-Skills
    "https://arxiv.org/abs/2604.24300",  # ReVSI: Rebuilding Visual Spatial Intelligence Evaluation for Accurate Assessment of VLM 3D Reasoning
    "https://arxiv.org/abs/2604.24391",  # FreqCache: Accelerating Embodied VLN Models with Adaptive Frequency-Guided Token Caching
    "https://arxiv.org/abs/2604.24532",  # A Reward-Free Viewpoint on Multi-Objective Reinforcement Learning
    "https://arxiv.org/abs/2604.24583",  # Improving Vision-language Models with Perception-centric Process Reward Models
    "https://arxiv.org/abs/2604.24661",  # Agent-Centric Visual Reinforcement Learning under Dynamic Perturbations
    "https://arxiv.org/abs/2604.24681",  # Learning Human-Intention Priors from Large-Scale Human Demonstrations for Robotic Manipulation
    "https://arxiv.org/abs/2604.24763",  # Tuna-2: Pixel Embeddings Beat Vision Encoders for Multimodal Understanding and Generation
    "https://arxiv.org/abs/2604.24764",  # World-R1: Reinforcing 3D Constraints for Text-to-Video Generation
    "https://arxiv.org/abs/2604.24833",  # MotionBricks: Scalable Real-Time Motions with Modular Latent Generative Model and Smart Primitives
    "https://arxiv.org/abs/2604.24881",  # Latent Agents: A Post-Training Procedure for Internalized Multi-Agent Debate
    "https://arxiv.org/abs/2604.24916",  # asRoBallet: Closing the Sim2Real Gap via Friction-Aware Reinforcement Learning for Underactuated Spherical Dynamics
    "https://arxiv.org/abs/2604.25067",  # Frontier Coding Agents Can Now Implement an AlphaZero Self-Play Machine Learning Pipeline For Connect Four That Performs Comparably to an External Solver
    "https://arxiv.org/abs/2604.25135",  # FAMA: Failure-Aware Meta-Agentic Framework for Open-Source LLMs in Interactive Tool Use Environments
    "https://arxiv.org/abs/2604.25276",  # OmniVTG: A Large-Scale Dataset and Training Paradigm for Open-World Video Temporal Grounding
    "https://arxiv.org/abs/2604.25329",  # ProDrive: Proactive Planning for Autonomous Driving via Ego-Environment Co-Evolution
    "https://arxiv.org/abs/2604.25459",  # GS-Playground: A High-Throughput Photorealistic Simulator for Vision-Informed Robot Learning
    "https://arxiv.org/abs/2604.25636",  # Refinement via Regeneration: Enlarging Modification Space Boosts Image Refinement in Unified Multimodal Models
    "https://arxiv.org/abs/2604.25788",  # KinDER: A Physical Reasoning Benchmark for Robot Learning and Planning
    "https://arxiv.org/abs/2604.25850",  # Agentic Harness Engineering: Observability-Driven Automatic Evolution of Coding-Agent Harnesses
    "https://arxiv.org/abs/2604.25859",  # Privileged Foresight Distillation: Zero-Cost Future Correction for World Action Models
    "https://arxiv.org/abs/2604.26065",  # FlowS: One-Step Motion Prediction via Local Transport Conditioning
    "https://arxiv.org/abs/2604.26182",  # Lifting Embodied World Models for Planning and Control
    "https://arxiv.org/abs/2604.26262",  # Semantic Foam: Unifying Spatial and Semantic Scene Decomposition
    "https://arxiv.org/abs/2604.26341",  # SpatialFusion: Endowing Unified Image Generation with Intrinsic 3D Geometric Awareness
    "https://arxiv.org/abs/2604.26488",  # Featurising Pixels from Dynamic 3D Scenes with Linear In-Context Learners
    "https://arxiv.org/abs/2604.26504",  # HiPAN: Hierarchical Posture-Adaptive Navigation for Quadruped Robots in Unstructured 3D Environments
    "https://arxiv.org/abs/2604.26509",  # 3D Generation for Embodied AI and Robotic Simulation: A Survey
    "https://arxiv.org/abs/2604.26569",  # LLM-Flax: Generalizable Robotic Task Planning via Neuro-Symbolic Approaches with Large Language Models
    "https://arxiv.org/abs/2604.26694",  # Unified 4D World Action Modeling from Video Priors with Asynchronous Denoising
    "https://arxiv.org/abs/2604.26707",  # CurEvo: Curriculum-Guided Self-Evolution for Video Understanding
    "https://arxiv.org/abs/2604.26779",  # Accelerating RL Post-Training Rollouts via System-Integrated Speculative Decoding
    "https://arxiv.org/abs/2604.26848",  # STARRY: Spatial-Temporal Action-Centric World Modeling for Robotic Manipulation
    "https://arxiv.org/abs/2604.26934",  # World2VLM: Distilling World Model Imagination into VLMs for Dynamic Spatial Reasoning
    "https://arxiv.org/abs/2604.27063",  # Learning to Forget: Continual Learning with Adaptive Weight Decay
    "https://arxiv.org/abs/2604.27077",  # Learning Rate Transfer in Normalized Transformers
    "https://arxiv.org/abs/2604.27083",  # Co-Evolving Policy Distillation
    "https://arxiv.org/abs/2604.27085",  # Efficient Training on Multiple Consumer GPUs with RoundPipe
    "https://arxiv.org/abs/2604.27106",  # Reconstruction by Generation: 3D Multi-Object Scene Reconstruction from Sparse Observations
    "https://arxiv.org/abs/2604.27155",  # Generalizing the Geometry of Model Merging Through Frechet Averages
    "https://arxiv.org/abs/2604.27367",  # DOT-Sim: Differentiable Optical Tactile Simulation with Precise Real-to-Sim Physical Calibration
    "https://arxiv.org/abs/2604.27472",  # PRTS: A Primitive Reasoning and Tasking System via Contrastive Representations
    "https://arxiv.org/abs/2604.27488",  # Skills-Coach: A Self-Evolving Skill Optimizer via Training-Free GRPO
    "https://arxiv.org/abs/2604.27505",  # Leveraging Verifier-Based Reinforcement Learning in Image Editing
    "https://arxiv.org/abs/2604.27508",  # SASI: Leveraging Sub-Action Semantics for Robust Early Action Recognition in Human-Robot Interaction
    "https://arxiv.org/abs/2604.27621",  # Robot Learning from Human Videos: A Survey
    "https://arxiv.org/abs/2604.27711",  # ExoActor: Exocentric Video Generation as Generalizable Interactive Humanoid Control
    "https://arxiv.org/abs/2604.27792",  # MotuBrain: An Advanced World Action Model for Robot Control
    "https://arxiv.org/abs/2604.27859",  # Rethinking Agentic Reinforcement Learning In Large Language Models
    "https://arxiv.org/abs/2604.27998",  # Latent-GRPO: Group Relative Policy Optimization for Latent Reasoning
    "https://arxiv.org/abs/2604.28005",  # Kernelized Advantage Estimation: From Nonparametric Statistics to LLM Reasoning
    "https://arxiv.org/abs/2604.28119",  # Do Sparse Autoencoders Capture Concept Manifolds?
    "https://arxiv.org/abs/2604.28123",  # Beyond SFT-to-RL: Pre-alignment via Black-Box On-Policy Distillation for Multimodal RL
    "https://arxiv.org/abs/2604.28156",  # FlexiTac: A Low-Cost, Open-Source, Scalable Tactile Sensing Solution for Robotic Systems
    "https://arxiv.org/abs/2604.28158",  # Intern-Atlas: A Methodological Evolution Graph as Research Infrastructure for AI Scientists
    "https://arxiv.org/abs/2604.28169",  # PhyCo: Learning Controllable Physical Priors for Generative Motion
    "https://arxiv.org/abs/2604.28182",  # Exploration Hacking: Can LLMs Learn to Resist RL Training?
    "https://arxiv.org/abs/2604.28185",  # Visual Generation in the New Era: An Evolution from Atomic Mapping to Agentic World Modeling
    "https://arxiv.org/abs/2604.28190",  # Representation Fréchet Loss for Visual Generation
    "https://arxiv.org/abs/2604.28192",  # LaST-R1: Reinforcing Action via Adaptive Physical Latent Reasoning for VLA Models
    "https://arxiv.org/abs/2605.00078",  # Being-H0.7: A Latent World-Action Model from Egocentric Videos
    "https://arxiv.org/abs/2605.00080",  # World Model for Robot Learning: A Comprehensive Survey
    "https://arxiv.org/abs/2605.00416",  # Learning while Deploying: Fleet-Scale Reinforcement Learning for Generalist Robot Policies
    "https://arxiv.org/abs/2605.00781",  # Map2World: Segment Map Conditioned Text to 3D World Generation
    "https://arxiv.org/abs/2605.00814",  # Persistent Visual Memory: Sustaining Perception for Deep Generation in LVLMs
    "https://arxiv.org/abs/2605.00880",  # Adversarial Flow Matching for Imperceptible Attacks on End-to-End Autonomous Driving
    "https://arxiv.org/abs/2605.00891",  # X2SAM: Any Segmentation in Images and Videos
    "https://arxiv.org/abs/2605.01191",  # Sentinel-VLA: A Metacognitive VLA Model with Active Status Monitoring for Dynamic Reasoning and Error Recovery
    "https://arxiv.org/abs/2605.01324",  # Beyond Perceptual Shortcuts: Causal-Inspired Debiasing Optimization for Generalizable Video Reasoning in Lightweight MLLMs
    "https://arxiv.org/abs/2605.01663",  # Towards Efficient and Expressive Offline RL via Flow-Anchored Noise-conditioned Q-Learning
    "https://arxiv.org/abs/2605.01694",  # Latent State Design for World Models under Sufficiency Constraints
    "https://arxiv.org/abs/2605.01772",  # Anticipation-VLA: Solving Long-Horizon Embodied Tasks via Anticipation-based Subgoal Generation
    "https://arxiv.org/abs/2605.01799",  # Embody4D: A Generalist 4D World Model for Embodied AI
    "https://arxiv.org/abs/2605.01882",  # Chart-FR1: Visual Focus-Driven Fine-Grained Reasoning on Dense Charts
    "https://arxiv.org/abs/2605.02073",  # Enhanced LLM Reasoning by Optimizing Reward Functions with Search-Driven Reinforcement Learning
    "https://arxiv.org/abs/2605.02087",  # Model Spec Midtraining: Improving How Alignment Training Generalizes
    "https://arxiv.org/abs/2605.02134",  # Video Generation with Predictive Latents
    "https://arxiv.org/abs/2605.02306",  # Natural Gradient Bayesian Filtering: Geometry-Aware Filter for Dynamical Systems
    "https://arxiv.org/abs/2605.02487",  # Visibility-Aware Mobile Grasping in Dynamic Environments
    "https://arxiv.org/abs/2605.02600",  # CoRAL: Contact-Rich Adaptive LLM-based Control for Robotic Manipulation
    "https://arxiv.org/abs/2605.02641",  # Mamoda2.5: Enhancing Unified Multimodal Model with DiT-MoE
    "https://arxiv.org/abs/2605.02730",  # Perceptual Flow Network for Visually Grounded Reasoning
    "https://arxiv.org/abs/2605.02735",  # Visual Latents Know More Than They Say: Unsilencing Latent Reasoning in MLLMs
    "https://arxiv.org/abs/2605.02739",  # Latent Bridge: Feature Delta Prediction for Efficient Dual-System Vision-Language-Action Model Inference
    "https://arxiv.org/abs/2605.02757",  # Seeing Realism from Simulation: Efficient Video Transfer for Vision-Language-Action Data Augmentation
    "https://arxiv.org/abs/2605.02881",  # MolmoAct2: Action Reasoning Models for Real-world Deployment
    "https://arxiv.org/abs/2605.02900",  # Safety in Embodied AI: A Survey of Risks, Attacks, and Defenses
    "https://arxiv.org/abs/2605.03065",  # OGPO: Sample Efficient Full-Finetuning of Generative Control Policies
    "https://arxiv.org/abs/2605.03269",  # RLDX-1 Technical Report
    "https://arxiv.org/abs/2605.03276",  # VEBench:Benchmarking Large Multimodal Models for Real-World Video Editing
    "https://arxiv.org/abs/2605.03363",  # Learning Reactive Dexterous Grasping via Hierarchical Task-Space RL Planning and Joint-Space QP Control
    "https://arxiv.org/abs/2605.03413",  # Learning to Theorize the World from Observation
    "https://arxiv.org/abs/2605.03452",  # BifrostUMI: Bridging Robot-Free Demonstrations and Humanoid Whole-Body Manipulation
    "https://arxiv.org/abs/2605.03517",  # Understanding Self-Supervised Learning via Latent Distribution Matching
    "https://arxiv.org/abs/2605.03677",  # Uni-OPD: Unifying On-Policy Distillation with a Dual-Perspective Recipe
    "https://arxiv.org/abs/2605.03782",  # What You Think is What You See: Driving Exploration in VLM Agents via Visual-Linguistic Curiosity
    "https://arxiv.org/abs/2605.03808",  # Agentic-imodels: Evolving agentic interpretability tools via autoresearch
    "https://arxiv.org/abs/2605.03821",  # RoboAlign-R1: Distilled Multimodal Reward Alignment for Robot Video World Models
    "https://arxiv.org/abs/2605.03846",  # SigLoMa: Learning Open-World Quadrupedal Loco-Manipulation from Ego-Centric Vision
    "https://arxiv.org/abs/2605.03941",  # iWorld-Bench: A Benchmark for Interactive World Models with a Unified Action Generation Framework
    "https://arxiv.org/abs/2605.04128",  # Awaking Spatial Intelligence in Unified Multimodal Understanding and Generation
    "https://arxiv.org/abs/2605.04470",  # CRAFT: Counterfactual-to-Interactive Reinforcement Fine-Tuning for Driving Policies
    "https://arxiv.org/abs/2605.04568",  # Dream-MPC: Gradient-Based Model Predictive Control with Latent Imagination
    "https://arxiv.org/abs/2605.04678",  # From Pixels to Tokens: A Systematic Study of Latent Action Supervision for Vision-Language-Action Models
    "https://arxiv.org/abs/2605.04709",  # ELVIS: Ensemble-Calibrated Latent Imagination for Long-Horizon Visual MPC
    "https://arxiv.org/abs/2605.05017",  # Position: Embodied AI Requires a Privacy-Utility Trade-off
    "https://arxiv.org/abs/2605.05126",  # ConsisVLA-4D: Advancing Spatiotemporal Consistency in Efficient 3D-Perception and 4D-Reasoning for Robotic Manipulation
    "https://arxiv.org/abs/2605.05163",  # PhysForge: Generating Physics-Grounded 3D Assets for Interactive Virtual World
    "https://arxiv.org/abs/2605.05172",  # When Life Gives You BC, Make Q-functions: Extracting Q-values from Behavior Cloning for On-Robot Reinforcement Learning
    "https://arxiv.org/abs/2605.05204",  # D-OPSD: On-Policy Self-Distillation for Continuously Tuning Step-Distilled Diffusion Models
    "https://arxiv.org/abs/2605.05328",  # Query2Uncertainty: Robust Uncertainty Quantification and Calibration for 3D Object Detection under Distribution Shift
    "https://arxiv.org/abs/2605.05544",  # Adaptive Q-Chunking for Offline-to-Online Reinforcement Learning
    "https://arxiv.org/abs/2605.05756",  # MaMi-HOI: Harmonizing Global Kinematics and Local Geometry for Human-Object Interaction Generation
    "https://arxiv.org/abs/2605.05812",  # Long-Horizon Q-Learning: Accurate Value Learning via n-Step Inequalities
    "https://arxiv.org/abs/2605.05925",  # DexSynRefine: Synthesizing and Refining Human-Object Interaction Motion for Physically Feasible Dexterous Robot Actions
    "https://arxiv.org/abs/2605.05945",  # MobileEgo Anywhere: Open Infrastructure for long horizon egocentric data on commodity hardware
    "https://arxiv.org/abs/2605.06094",  # VISD: Enhancing Video Reasoning via Structured Self-Distillation
    "https://arxiv.org/abs/2605.06139",  # Listwise Policy Optimization: Group-based RLVR as Target-Projection on the LLM Response Simplex
    "https://arxiv.org/abs/2605.06175",  # VLA-GSE: Boosting Parameter-Efficient Fine-Tuning in VLA with Generalized and Specialized Experts
    "https://arxiv.org/abs/2605.06192",  # EA-WM: Event-Aware Generative World Model with Structured Kinematic-to-Visual Action Fields
    "https://arxiv.org/abs/2605.06222",  # When to Trust Imagination: Adaptive Action Execution for World Action Models
    "https://arxiv.org/abs/2605.06234",  # RobotEQ: Transitioning from Passive Intelligence to Active Intelligence in Embodied AI
    "https://arxiv.org/abs/2605.06247",  # CKT-WAM: Parameter-Efficient Context Knowledge Transfer Between World Action Models
    "https://arxiv.org/abs/2605.06311",  # Toward Visually Realistic Simulation: A Benchmark for Evaluating Robot Manipulation in Simulation
    "https://arxiv.org/abs/2605.06388",  # Reconstruction or Semantics? What Makes a Latent Space Useful for Robotic World Models
    "https://arxiv.org/abs/2605.06481",  # OA-WAM: Object-Addressable World Action Model for Robust Robot Manipulation
    "https://arxiv.org/abs/2605.06507",  # MARBLE: Multi-Aspect Reward Balance for Diffusion RL
    "https://arxiv.org/abs/2605.06593",  # ReActor: Reinforcement Learning for Physics-Aware Motion Retargeting
    "https://arxiv.org/abs/2605.06595",  # Cross-Modal Navigation with Multi-Agent Reinforcement Learning
    "https://arxiv.org/abs/2605.06614",  # SkillOS: Learning Skill Curation for Self-Evolving Agents
    "https://arxiv.org/abs/2605.06732",  # On Training in Imagination
    "https://arxiv.org/abs/2605.06747",  # HumanNet: Scaling Human-centric Video Learning to One Million Hours
    "https://arxiv.org/abs/2605.06758",  # R$^3$L: Reasoning 3D Layouts from Relative Spatial Relations
    "https://arxiv.org/abs/2605.06840",  # Extracting Search Trees from LLM Reasoning Traces Reveals Myopic Planning
    "https://arxiv.org/abs/2605.07177",  # HyperEyes: Dual-Grained Efficiency-Aware Reinforcement Learning for Parallel Multimodal Search Agents
    "https://arxiv.org/abs/2605.07308",  # AT-VLA: Adaptive Tactile Injection for Enhanced Feedback Reaction in Vision-Language-Action Models
    "https://arxiv.org/abs/2605.07396",  # Rubric-based On-policy Distillation
    "https://arxiv.org/abs/2605.07429",  # Towards Photorealistic and Efficient Bokeh Rendering via Diffusion Framework
    "https://arxiv.org/abs/2605.07465",  # SEIF: Self-Evolving Reinforcement Learning for Instruction Following
    "https://arxiv.org/abs/2605.07943",  # TAVIS: A Benchmark for Egocentric Active Vision and Anticipatory Gaze in Imitation Learning
    "https://arxiv.org/abs/2605.08064",  # Proxy3D: Efficient 3D Representations for Vision-Language Models via Semantic Clustering and Alignment
    "https://arxiv.org/abs/2605.08078",  # Normalizing Trajectory Models
    "https://arxiv.org/abs/2605.08083",  # LLMs Improving LLMs: Agentic Discovery for Test-Time Scaling
    "https://arxiv.org/abs/2605.08202",  # Beyond Penalization: Diffusion-based Out-of-Distribution Detection and Selective Regularization in Offline Reinforcement Learning
    "https://arxiv.org/abs/2605.08215",  # Test-Time Training for Visual Foresight Vision-Language-Action Models
    "https://arxiv.org/abs/2605.08434",  # Failing Forward: Adaptive Failure-Informed Learning for Vision-Language-Action Models
    "https://arxiv.org/abs/2605.08567",  # ACWM-Phys: Investigating Generalized Physical Interaction in Action-Conditioned Video World Models
    "https://arxiv.org/abs/2605.08732",  # Latent Geometry Beyond Search: Amortizing Planning in World Models
    "https://arxiv.org/abs/2605.08774",  # ProcVLM: Learning Procedure-Grounded Progress Rewards for Robotic Manipulation
    "https://arxiv.org/abs/2605.08799",  # ElasticFlow: One-Step Physics-Consistent Policy with Elastic Time Horizons for Language-Guided Manipulation
    "https://arxiv.org/abs/2605.08879",  # Preserving Foundational Capabilities in Flow-Matching VLAs through Conservative SFT
    "https://arxiv.org/abs/2605.09131",  # MCP-Cosmos: World Model-Augmented Agents for Complex Task Execution in MCP Environments
    "https://arxiv.org/abs/2605.09196",  # RigidFormer: Learning Rigid Dynamics using Transformers
    "https://arxiv.org/abs/2605.09218",  # Flame3D: Zero-shot Compositional Reasoning of 3D Scenes with Agentic Language Models
    "https://arxiv.org/abs/2605.09387",  # NEXUS: Continual Learning of Symbolic Constraints for Safe and Robust Embodied Planning
    "https://arxiv.org/abs/2605.09410",  # RePO-VLA: Recovery-Driven Policy Optimization for Vision-Language-Action Models
    "https://arxiv.org/abs/2605.09537",  # Drift is a Sampling Error: SNR-Aware Power Distributions for Long-Horizon Robotic Planning
    "https://arxiv.org/abs/2605.09538",  # PhysHanDI: Physics-Based Reconstruction of Hand-Deformable Object Interactions
    "https://arxiv.org/abs/2605.09613",  # SABER: A Scalable Action-Based Embodied Dataset for Real-World VLA Adaptation
    "https://arxiv.org/abs/2605.09772",  # Safe Exploration for Nonlinear Processes Using Online Gaussian Process Learning
    "https://arxiv.org/abs/2605.09789",  # Zero-Shot Sim-to-Real Robot Learning: A Dexterous Manipulation Study on Reactive Catching
    "https://arxiv.org/abs/2605.09948",  # LoopVLA: Learning Sufficiency in Recurrent Refinement for Vision-Language-Action Models
    "https://arxiv.org/abs/2605.09954",  # JODA: Composable Joint Dynamics for Articulated Objects
    "https://arxiv.org/abs/2605.09963",  # Learning to Perceive "Where": Spatial Pretext Tasks for Robust Self-Supervised Learning
    "https://arxiv.org/abs/2605.10051",  # Guided Streaming Stochastic Interpolant Policy
    "https://arxiv.org/abs/2605.10063",  # EFGCL: Learning Dynamic Motion through Spotting-Inspired External Force Guided Curriculum Learning
    "https://arxiv.org/abs/2605.10118",  # Plan in Sandbox, Navigate in Open Worlds: Learning Physics-Grounded Abstracted Experience for Embodied Navigation
    "https://arxiv.org/abs/2605.10204",  # 3DReflecNet: A Large-Scale Dataset for 3D Reconstruction of Reflective, Transparent, and Low-Texture Objects
    "https://arxiv.org/abs/2605.10485",  # VEGA: Visual Encoder Grounding Alignment for Spatially-Aware Vision-Language-Action Models
    "https://arxiv.org/abs/2605.10663",  # Evolving-RL: End-to-End Optimization of Experience-Driven Self-Evolving Capability within Agents
    "https://arxiv.org/abs/2605.10759",  # Reinforce Adjoint Matching: Scaling RL Post-Training of Diffusion and Flow-Matching Models
    "https://arxiv.org/abs/2605.10819",  # ALAM: Algebraically Consistent Latent Action Model for Vision-Language-Action Models
    "https://arxiv.org/abs/2605.10889",  # Unmasking On-Policy Distillation: Where It Helps, Where It Hurts, and Why
    "https://arxiv.org/abs/2605.10903",  # CapVector: Learning Transferable Capability Vectors in Parametric Space for Vision-Language-Action Models
    "https://arxiv.org/abs/2605.10921",  # RoboMemArena: A Comprehensive and Challenging Robotic Memory Benchmark
    "https://arxiv.org/abs/2605.10925",  # PriorVLA: Prior-Preserving Adaptation for Vision-Language-Action Models
    "https://arxiv.org/abs/2605.10942",  # HarmoWAM: Harmonizing Generalizable and Precise Manipulation via Adaptive World Action Models
    "https://arxiv.org/abs/2605.10993",  # ECHO: Continuous Hierarchical Memory for Vision-Language-Action Models
    "https://arxiv.org/abs/2605.11009",  # ACSAC: Adaptive Chunk Size Actor-Critic with Causal Transformer Q-Network
    "https://arxiv.org/abs/2605.11020",  # Trust Region Inverse Reinforcement Learning: Explicit Dual Ascent using Local Policy Updates
    "https://arxiv.org/abs/2605.11151",  # RankQ: Offline-to-Online Reinforcement Learning via Self-Supervised Action Ranking
    "https://arxiv.org/abs/2605.11182",  # The Many Faces of On-Policy Distillation: Pitfalls, Mechanisms, and Fixes
    "https://arxiv.org/abs/2605.11367",  # 3D-Belief: Embodied Belief Inference via Generative 3D World Modeling
    "https://arxiv.org/abs/2605.11381",  # Kairos: A Scalable Serving System for Physical AI
    "https://arxiv.org/abs/2605.11473",  # TOPPO: Rethinking PPO for Multi-Task Reinforcement Learning with Critic Balancing
    "https://arxiv.org/abs/2605.11564",  # RIO: Flexible Real-Time Robot I/O for Cross-Embodiment Robot Learning
    "https://arxiv.org/abs/2605.11609",  # Anti-Self-Distillation for Reasoning RL via Pointwise Mutual Information
    "https://arxiv.org/abs/2605.11689",  # Slicing and Dicing: Configuring Optimal Mixtures of Experts
    "https://arxiv.org/abs/2605.11739",  # Learning to Foresee: Unveiling the Unlocking Efficiency of On-Policy Distillation
    "https://arxiv.org/abs/2605.11832",  # Learning Action Manifold with Multi-view Latent Priors for Robotic Manipulation
    "https://arxiv.org/abs/2605.11856",  # UniVLR: Unifying Text and Vision in Visual Latent Reasoning for Multimodal LLMs
    "https://arxiv.org/abs/2605.12090",  # World Action Models: The Next Frontier in Embodied AI
    "https://arxiv.org/abs/2605.12167",  # From Imagined Futures to Executable Actions: Mixture of Latent Actions for Robot Manipulation
    "https://arxiv.org/abs/2605.12227",  # Combining On-Policy Optimization and Distillation for Long-Context Reasoning in Large Language Models
    "https://arxiv.org/abs/2605.12369",  # GuidedVLA: Specifying Task-Relevant Factors via Plug-and-Play Action Attention Specialization
    "https://arxiv.org/abs/2605.12466",  # Solve the Loop: Attractor Models for Language and Reasoning
    "https://arxiv.org/abs/2605.12474",  # Reward Hacking in Rubric-Based Reinforcement Learning
    "https://arxiv.org/abs/2605.12483",  # Beyond GRPO and On-Policy Distillation: An Empirical Sparse-to-Dense Reward Principle for Language-Model Post-Training
    "https://arxiv.org/abs/2605.12484",  # Learning, Fast and Slow: Towards LLMs That Adapt Continually
    "https://arxiv.org/abs/2605.12654",  # COSMIC: Concurrent Optimization of Structure, Material, and Integrated Control for robotic systems
    "https://arxiv.org/abs/2605.12689",  # 3D RL-DWA: A Hybrid Reinforcement Learning and Dynamic Window Approach for Goal-Directed Local Navigation in Multi-DoF Robots
    "https://arxiv.org/abs/2605.12733",  # From Generalist to Specialist Representation
    "https://arxiv.org/abs/2605.12741",  # Learning with Rare Success but Rich Feedback via Reflection-Enhanced Self-Distillation
    "https://arxiv.org/abs/2605.12771",  # Adaptive Smooth Tchebycheff Attention for Multi-Objective Policy Optimization
    "https://arxiv.org/abs/2605.13083",  # TouchAnything: A Dataset and Framework for Bimanual Tactile Estimation from Egocentric Video
    "https://arxiv.org/abs/2605.13105",  # What to Ignore, What to React: Visually Robust RL Fine-Tuning of VLA Models
    "https://arxiv.org/abs/2605.13119",  # Towards Long-horizon Embodied Agents with Tool-Aligned Vision-Language-Action Models
    "https://arxiv.org/abs/2605.13276",  # D-VLA: A High-Concurrency Distributed Asynchronous Reinforcement Learning Framework for Vision-Language-Action Models
    "https://arxiv.org/abs/2605.13403",  # RotVLA: Rotational Latent Action for Vision-Language-Action Model
    "https://arxiv.org/abs/2605.13452",  # CUBic: Coordinated Unified Bimanual Perception and Control Framework
    "https://arxiv.org/abs/2605.13467",  # PDCR: Perception-Decomposed Confidence Reward for Vision-Language Reasoning
    "https://arxiv.org/abs/2605.13632",  # Guide, Think, Act: Interactive Embodied Reasoning in Vision-Language-Action Models
    "https://arxiv.org/abs/2605.13724",  # AnyFlow: Any-Step Video Diffusion Model with On-Policy Flow Map Distillation
    "https://arxiv.org/abs/2605.13775",  # RoboEvolve: Co-Evolving Planner-Simulator for Robotic Manipulation with Limited Data
    "https://arxiv.org/abs/2605.13778",  # Realtime-VLA FLASH: Speculative Inference Framework for Diffusion-based VLAs
    "https://arxiv.org/abs/2605.13959",  # WarmPrior: Straightening Flow-Matching Policies with Temporal Priors
    "https://arxiv.org/abs/2605.14174",  # Safety-Constrained Reinforcement Learning with Post-Training Reachability Verification for Robot Navigation
    "https://arxiv.org/abs/2605.14386",  # Darwin Family: MRI-Trust-Weighted Evolutionary Merging for Training-Free Scaling of Language-Model Reasoning
    "https://arxiv.org/abs/2605.14417",  # Before the Body Moves: Learning Anticipatory Joint Intent for Language-Conditioned Humanoid Control
    "https://arxiv.org/abs/2605.14539",  # Learning from Failures: Correction-Oriented Policy Optimization with Verifiable Rewards
    "https://arxiv.org/abs/2605.14571",  # Let Robots Feel Your Touch: Visuo-Tactile Cortical Alignment for Embodied Mirror Resonance
    "https://arxiv.org/abs/2605.14598",  # DSSP: Diffusion State Space Policy with Full-History Encoding
    "https://arxiv.org/abs/2605.14712",  # IntentVLA: Short-Horizon Intent Modeling for Aliased Robot Manipulation
    "https://arxiv.org/abs/2605.14733",  # Video-Zero: Self-Evolution Video Understanding
    "https://arxiv.org/abs/2605.14742",  # EARL: Towards a Unified Analysis-Guided Reinforcement Learning Framework for Egocentric Interaction Reasoning and Pixel Grounding
    "https://arxiv.org/abs/2605.14779",  # Peng's Q($λ$) for Conservative Value Estimation in Offline Reinforcement Learning
    "https://arxiv.org/abs/2605.14810",  # CaMeRL: Collision-Aware and Memory-Enhanced Reinforcement Learning for UAV Navigation in Multi-Scale Obstacle Environments
    "https://arxiv.org/abs/2605.14938",  # Octopus: History-Free Gradient Orthogonalization for Continual Learning in Multimodal Large Language Models
    "https://arxiv.org/abs/2605.14950",  # Evo-Depth: A Lightweight Depth-Enhanced Vision-Language-Action Model
    "https://arxiv.org/abs/2605.15012",  # Boosting Reinforcement Learning with Verifiable Rewards via Randomly Selected Few-Shot Guidance
    "https://arxiv.org/abs/2605.15055",  # DiffusionOPD: A Unified Perspective of On-Policy Distillation in Diffusion Models
    "https://arxiv.org/abs/2605.15128",  # MemEye: A Visual-Centric Evaluation Framework for Multimodal Agent Memory
    "https://arxiv.org/abs/2605.15153",  # Pelican-Unified 1.0: A Unified Embodied Intelligence Model for Understanding, Reasoning, Imagination and Action
    "https://arxiv.org/abs/2605.15155",  # Self-Distilled Agentic Reinforcement Learning
    "https://arxiv.org/abs/2605.15157",  # Hand-in-the-Loop: Improving Dexterous VLA via Seamless Interventional Correction
    "https://arxiv.org/abs/2605.15178",  # SANA-WM: Efficient Minute-Scale World Modeling with Hybrid Linear Diffusion Transformer
    "https://arxiv.org/abs/2605.15188",  # FutureSim: Replaying World Events to Evaluate Adaptive Agents
    "https://arxiv.org/abs/2605.15198",  # ATLAS: Agentic or Latent Visual Reasoning? One Word is Enough for Both
    "https://arxiv.org/abs/2605.15220",  # Always Learning, Always Mixing: Efficient and Simple Data Mixing All The Time
    "https://arxiv.org/abs/2605.15298",  # PhysBrain 1.0 Technical Report
    "https://arxiv.org/abs/2605.15458",  # Video Models Can Reason with Verifiable Rewards
    "https://arxiv.org/abs/2605.15618",  # Latent Video Prediction Learns Better World Models
    "https://arxiv.org/abs/2605.15725",  # DiLA: Disentangled Latent Action World Models
    "https://arxiv.org/abs/2605.15726",  # Nudging Beyond the Comfort Zone: Efficient Strategy-Guided Exploration for RLVR
    "https://arxiv.org/abs/2605.15735",  # UAM: A Dual-Stream Perspective on Forgetting in VLA Training
    "https://arxiv.org/abs/2605.15855",  # Do Less, Achieve More: Do We Need Every-Step Optimization for RL Fine-tuning of Diffusion Models?
    "https://arxiv.org/abs/2605.15951",  # From Failure to Feedback: Group Revision Unlocks Hard Cases in Object-Level Grounding
    "https://arxiv.org/abs/2605.16056",  # Health-Conditioned Vision-Language-Action Models for Malfunction-Aware Robot Control
    "https://arxiv.org/abs/2605.16257",  # DexJoCo: A Benchmark and Toolkit for Task-Oriented Dexterous Manipulation on MuJoCo
    "https://arxiv.org/abs/2605.16787",  # The Unlearnability Phenomenon in RLVR for Language Models
    "https://arxiv.org/abs/2605.17807",  # Curriculum Group Policy Optimization: Adaptive Sampling for Unleashing the Potential of Text-to-Image Generation
    "https://arxiv.org/abs/2605.18162",  # Self-Evolving Spatial Reasoning in Vision Language Models via Geometric Logic Consistency
    "https://arxiv.org/abs/2605.18233",  # Enhancing Train-Free Infinite-Frame Generation for Consistent Long Videos
    "https://arxiv.org/abs/2605.18678",  # Lance: Unified Multimodal Modeling by Multi-Task Synergy
    "https://arxiv.org/abs/2605.18722",  # Dexora: Open-source VLA for High-DoF Bimanual Dexterity
    "https://arxiv.org/abs/2605.18740",  # Vision-OPD: Learning to See Fine Details for Multimodal LLMs via On-Policy Self-Distillation
    "https://arxiv.org/abs/2605.18746",  # ESI-Bench: Towards Embodied Spatial Intelligence that Closes the Perception-Action Loop
    "https://arxiv.org/abs/2605.18813",  # Composition of Memory Experts for Diffusion World Models
    "https://arxiv.org/abs/2605.19033",  # RLFTSim: Realistic and Controllable Multi-Agent Traffic Simulation via Reinforcement Learning Fine-Tuning
    "https://arxiv.org/abs/2605.19282",  # Rethinking Muon Beyond Pretraining: Spectral Failures and High-Pass Remedies for VLA and RLVR
    "https://arxiv.org/abs/2605.19376",  # Generative Recursive Reasoning
    "https://arxiv.org/abs/2605.19919",  # Beyond Action Residuals: Real-World Robot Policy Steering via Bottleneck Latent Reinforcement Learning
    "https://arxiv.org/abs/2605.19924",  # RoHIL: Robust Human-in-the-Loop Robotic Reinforcement Learning Against Illumination Variations
    "https://arxiv.org/abs/2605.19957",  # World-Ego Modeling for Long-Horizon Evolution in Hybrid Embodied Tasks
    "https://arxiv.org/abs/2605.19986",  # Beyond Binary Success: A Diagnostic Meta-Evaluation Framework for Fine-Grained Manipulation
    "https://arxiv.org/abs/2605.20025",  # AutoResearchClaw: Self-Reinforcing Autonomous Research with Human-AI Collaboration
    "https://arxiv.org/abs/2605.20246",  # GROW: Aligning GRPO with State-Action Modeling for Open-World VLM Agents
    "https://arxiv.org/abs/2605.20284",  # JUDO: A Juxtaposed Domain-Oriented Multimodal Reasoner for Industrial Anomaly QA
    "https://arxiv.org/abs/2605.20290",  # TelePhysics: Physics-Grounded Multi-Object Scene Generation from a Single Image with Real-Time Interaction
    "https://arxiv.org/abs/2605.20373",  # SUGAR: A Scalable Human-Video-Driven Generalizable Humanoid Loco-Manipulation Learning Framework
    "https://arxiv.org/abs/2605.20752",  # GaussianDream: A Feed-Forward 3D Gaussian World Model for Robotic Manipulation
    "https://arxiv.org/abs/2605.20758",  # Conflict-Aware Additive Guidance for Flow Models under Compositional Rewards
    "https://arxiv.org/abs/2605.20774",  # VLA-REPLICA: A Low-Cost, Reproducible Benchmark for Real-World Evaluation of Vision-Language-Action Models
    "https://arxiv.org/abs/2605.20811",  # Demo-JEPA: Joint-Embedding Predictive Architecture for One-shot Cross-Embodiment Imitation
    "https://arxiv.org/abs/2605.20914",  # RISE: Reliable Improvement in Self-Evolving Vision-Language Models
    "https://arxiv.org/abs/2605.21061",  # Grounding Driving VLA via Inverse Kinematics
    "https://arxiv.org/abs/2605.21133",  # Humanoid Whole-Body Manipulation via Active Spatial Brain and Generalizable Action Cerebellum
    "https://arxiv.org/abs/2605.21258",  # Learning Structural Latent Points for Efficient Visual Representations in Robotic Manipulation
    "https://arxiv.org/abs/2605.21330",  # Learning Robust Dexterous In-Hand Manipulation from Joint Sensors with Proprioceptive Transformer
    "https://arxiv.org/abs/2605.21414",  # PointACT: Vision-Language-Action Models with Multi-Scale Point-Action Interaction
    "https://arxiv.org/abs/2605.21429",  # roto 2.0: The Robot Tactile Olympiad
    "https://arxiv.org/abs/2605.21467",  # DelTA: Discriminative Token Credit Assignment for Reinforcement Learning from Verifiable Rewards
    "https://arxiv.org/abs/2605.21572",  # PhysX-Omni: Unified Simulation-Ready Physical 3D Generation for Rigid, Deformable, and Articulated Objects
    "https://arxiv.org/abs/2605.21688",  # Closed-Loop Sim-to-Real Reinforcement Learning for Deformable Microfiber Shape Control
    "https://arxiv.org/abs/2605.21699",  # X-Token: Projection-Guided Cross-Tokenizer Knowledge Distillation
    "https://arxiv.org/abs/2605.21710",  # PGDG: Physically Grounded Data Generation for Robust Bimanual Policy Learning from a Single Demonstration
    "https://arxiv.org/abs/2605.21800",  # stable-worldmodel: A Platform for Reproducible World Modeling Research and Evaluation
    "https://arxiv.org/abs/2605.21811",  # Safe and Steerable Geometric Motion Policies for Robotic Dexterous Manipulation
    "https://arxiv.org/abs/2605.21854",  # CrossVLA: Cross-Paradigm Post-Training and Inference Optimization for Vision-Language-Action Models
    "https://arxiv.org/abs/2605.21862",  # EvoScene-VLA: Evolving Scene Beliefs Inside the Action Decoder for Chunked Robot Control
    "https://arxiv.org/abs/2605.21931",  # EvoVid: Temporal-Centric Self-Evolution for Video Large Language Models
    "https://arxiv.org/abs/2605.21935",  # Learning to Evolve: Multi-modal Interactive Fields for Robust Humanoid Navigation in Dynamic Environments
    "https://arxiv.org/abs/2605.21973",  # Foresee-to-Ground: From Predictive Temporal Perception to Evidence-Driven Reasoning for Video Temporal Grounding
    "https://arxiv.org/abs/2605.22123",  # Beyond Pixels: Learning Invariant Rewards for Real-World Robotics From a Few Demonstrations
    "https://arxiv.org/abs/2605.22138",  # Efficient Agentic Reasoning Through Self-Regulated Simulative Planning
    "https://arxiv.org/abs/2605.22183",  # Action with Visual Primitives
    "https://arxiv.org/abs/2605.22217",  # Survive or Collapse: The Asymmetric Roles of Data Gating and Reward Grounding in Self-Play RL
    "https://arxiv.org/abs/2605.22272",  # Imagine2Real: Towards Zero-shot Humanoid-Object Interaction via Video Generative Priors
    "https://arxiv.org/abs/2605.22283",  # Spatial Memory for Out-of-Vision Manipulation in Vision-Language-Action
    "https://arxiv.org/abs/2605.22297",  # One LR Doesn't Fit All: Heavy-Tail Guided Layerwise Learning Rates for LLMs
    "https://arxiv.org/abs/2605.22446",  # Pre-VLA: Preemptive Runtime Verification for Reliable Vision-Language-Action and World-Model Rollouts
    "https://arxiv.org/abs/2605.22536",  # SpaceDG: Benchmarking Spatial Intelligence under Visual Degradation
    "https://arxiv.org/abs/2605.22570",  # VGenST-Bench: A Benchmark for Spatio-Temporal Reasoning via Active Video Synthesis
    "https://arxiv.org/abs/2605.22629",  # H-Flow: Self-supervised Human Scene Flow via Physics-inspired Joint Multi-modal Learning
    "https://arxiv.org/abs/2605.22658",  # SegCompass: Exploring Interpretable Alignment with Sparse Autoencoders for Enhanced Reasoning Segmentation
    "https://arxiv.org/abs/2605.22671",  # From Abstraction to Instantiation: Learning Behavioral Representation for Vision-Language-Action Model
    "https://arxiv.org/abs/2605.22812",  # GesVLA: Gesture-Aware Vision-Language-Action Model Embedded Representations
    "https://arxiv.org/abs/2605.22814",  # Remember to be Curious: Episodic Context and Persistent Worlds for 3D Exploration
    "https://arxiv.org/abs/2605.22816",  # AwareVLN: Reasoning with Self-awareness for Vision-Language Navigation
    "https://arxiv.org/abs/2605.22817",  # Vector Policy Optimization: Training for Diversity Improves Test-Time Search
    "https://arxiv.org/abs/2605.22896",  # Agentic-VLA: Efficient Online Adaptation for Vision-Language-Action Models
    "https://arxiv.org/abs/2605.23733",  # Any2Any: Efficient Cross-Embodiment Transfer for Humanoid Whole-Body Tracking
    "https://arxiv.org/abs/2605.23895",  # From Activation to Causality: Discovery of Causal Visual Representations in the Human Brain
    "https://arxiv.org/abs/2605.23993",  # Nano World Models: A Minimalist Implementation of Future Video Prediction
    "https://arxiv.org/abs/2605.24642",  # Understanding the Impact of Geometric Foundation Models on Vision-Language-Action Models
    "https://arxiv.org/abs/2605.24934",  # HumanEgo: Zero-Shot Robot Learning from Minutes of Human Egocentric Videos
    "https://arxiv.org/abs/2605.24975",  # Bridging the Gap: Enabling Soft Actor Critic for High Performance Legged Locomotion
    "https://arxiv.org/abs/2605.25044",  # X-DiffVLA: X-Embodied Diffusion Action Heads for Vision-Language-Action Models
    "https://arxiv.org/abs/2605.25313",  # UWM-JEPA: Predictive World Models That Imagine in Belief Space
    "https://arxiv.org/abs/2605.25477",  # EXPO-FT: Sample-Efficient Reinforcement Learning Finetuning for Vision-Language-Action Models
    "https://arxiv.org/abs/2605.25495",  # RepSAM: Bridging Foundation Models to Robotic Vision via Representation-Guided Adaptation
    "https://arxiv.org/abs/2605.25537",  # Action-Prior Denoising for Smooth Real-Time Chunking
    "https://arxiv.org/abs/2605.25546",  # Safety-Critical Whole-Body Control for Humanoid Robots via Input-to-State Safe Control Barrier Functions
    "https://arxiv.org/abs/2605.25685",  # HumanFlow -- Diffusion-Driven MAV Navigation Among Humans via Tightly-Coupled Motion Tracking, Forecasting, and Control
    "https://arxiv.org/abs/2605.25813",  # Extending Embodied Question Answering from Perception to Decision
    "https://arxiv.org/abs/2605.25829",  # OASIS: Observation-Action Space Alignment via SE(3) Trajectory Prediction for Robotic Manipulation
    "https://arxiv.org/abs/2605.25832",  # When Search Becomes Memory: Turning Robot Design Trials into Transferable Skills
    "https://arxiv.org/abs/2605.25874",  # WBench: A Comprehensive Multi-turn Benchmark for Interactive Video World Model Evaluation
    "https://arxiv.org/abs/2605.26006",  # MIND: Multi-Scale Intent Diffusion for Text-Driven Physics-Based Humanoid Control
    "https://arxiv.org/abs/2605.26115",  # TriSplat: Simulation-Ready Feed-Forward 3D Scene Reconstruction
    "https://arxiv.org/abs/2605.26379",  # When Does LeJEPA Learn a World Model?
    "https://arxiv.org/abs/2605.26452",  # Robust Koopman Control Barrier Filters for Safe Actor-Critic Reinforcement Learning
    "https://arxiv.org/abs/2605.26478",  # Efficient On-policy Visual-RL via Stochastic Decoupled Policy Gradient
    "https://arxiv.org/abs/2605.26494",  # The MiniMax-M2 Series: Mini Activations Unleashing Max Real-World Intelligence
    "https://arxiv.org/abs/2605.26535",  # Recursive Flow Matching
    "https://arxiv.org/abs/2605.26637",  # Enabling Extensible Embodied Capabilities with Tools
    "https://arxiv.org/abs/2605.26638",  # HyperSim: A Holistic Sim-To-Real Framework For Robust Robotic Manipulation
    "https://arxiv.org/abs/2605.26656",  # DV-SFT: Direct Vision Supervision for Fine-Grained Visual Understanding
    "https://arxiv.org/abs/2605.26820",  # Can VLA Models Learn from Real-World Data Continually without Forgetting?
    "https://arxiv.org/abs/2605.27020",  # Black-box Membership Inference Attacks on the Pre-training Data of Image-generation Models
    "https://arxiv.org/abs/2605.27046",  # Learning to Balance Motor Thermal Safety and Quadrupedal Locomotion Performance with Residual Policy
    "https://arxiv.org/abs/2605.27079",  # Trust Region Q Adjoint Matching
    "https://arxiv.org/abs/2605.27114",  # VR-DAgger: Immersive VR for Dexterous Data Collection and Uncertainty-Guided On-Policy Correction
    "https://arxiv.org/abs/2605.27276",  # SIA: Self Improving AI with Harness & Weight Updates
    "https://arxiv.org/abs/2605.27284",  # FineVLA: Fine-Grained Instruction Alignment for Steerable Vision-Language-Action Policies
    "https://arxiv.org/abs/2605.27365",  # LocateAnything: Fast and High-Quality Vision-Language Grounding with Parallel Box Decoding
    "https://arxiv.org/abs/2605.27367",  # SpatialBench: Is Your Spatial Foundation Model an All-Round Player?
    "https://arxiv.org/abs/2605.27491",  # GE-Sim 2.0: A Roadmap Towards Comprehensive Closed-loop Video World Simulators for Robotic Manipulation
    "https://arxiv.org/abs/2605.27589",  # What-If World: A Causal Benchmark for General World Models in Embodied Scenarios
    "https://arxiv.org/abs/2605.27724",  # HumanoidMimicGen: Data Generation for Loco-Manipulation via Whole-Body Planning
    "https://arxiv.org/abs/2605.27734",  # Learn from your own latents and not from tokens: A sample-complexity theory
    "https://arxiv.org/abs/2605.28293",  # ProRL: Effective Reinforcement Learning for Proactive Recommendation via Rectified Policy Gradient Estimation
    "https://arxiv.org/abs/2605.28421",  # DenoiseRL: Bootstrapping Reasoning Models to Recover from Noisy Prefixes
    "https://arxiv.org/abs/2605.28442",  # Self-Supervised Online Robot-Agnostic Traversability Estimation for Open-World Environments
    "https://arxiv.org/abs/2605.28527",  # What Frozen VLAs Already Know About Success: A Probing Study of Value-Like Structure in Foundation Robot Policies
    "https://arxiv.org/abs/2605.28634",  # PrimitiveVLA: Learning Reusable Motion Primitives for Efficient and Generalizable Robotic Manipulation
    "https://arxiv.org/abs/2605.28774",  # Agent Explorative Policy Optimization for Multimodal Agentic Reasoning
    "https://arxiv.org/abs/2605.28812",  # Beyond Binary: Sim-to-Real Dexterous Manipulation with Physics-Grounded Contact Representation
    "https://arxiv.org/abs/2605.28814",  # Self-Improving Language Models with Bidirectional Evolutionary Search
    "https://arxiv.org/abs/2605.28816",  # Gamma-World: Generative Multi-Agent World Modeling Beyond Two Players
    "https://arxiv.org/abs/2605.28820",  # From Pixels to Words -- Towards Native One-Vision Models at Scale
    "https://arxiv.org/abs/2605.28828",  # Micro-Macro Retrieval: Reducing Long-Form Hallucination in Large Language Models
    "https://arxiv.org/abs/2605.29074",  # Embodied3DBench: Benchmarking Low-Level Embodied Spatial Intelligence of Vision Language Models
    "https://arxiv.org/abs/2605.29198",  # Guidance Contrastive Token Credit Assignment for Discrete Policy Optimization
    "https://arxiv.org/abs/2605.29341",  # WorldMemArena: Evaluating Multimodal Agent Memory Through Action-World Interaction
    "https://arxiv.org/abs/2605.29360",  # MiraBench: Evaluating Action-Conditioned Reliability in Robotic World Models
    "https://arxiv.org/abs/2605.29416",  # 3DVLA: Enhancing Vision-Language-Action Models via 3D Spatial and Instance Understanding
    "https://arxiv.org/abs/2605.29438",  # ElegantVLA: Learning When to Think for Efficient Vision-Language-Action Models
    "https://arxiv.org/abs/2605.29548",  # Why Larger Models Learn More: Effects of Capacity, Interference, and Rare-Task Retention
    "https://arxiv.org/abs/2605.29562",  # VLA-Pro: Cross-Task Procedural Memory Transfer for Vision-Language-Action Models
    "https://arxiv.org/abs/2605.29563",  # Planning with the Views via Scene Self-Exploration
    "https://arxiv.org/abs/2605.29564",  # VE2VF: Vision-Enabled to Vision-Free Distillation via Real-world Reinforcement Learning for Robust Contact-Rich Manipulation
    "https://arxiv.org/abs/2605.29710",  # PhAIL: A Real-Robot VLA Benchmark and Distributional Methodology
    "https://arxiv.org/abs/2605.30056",  # Sample-Efficient Diffusion-based Reinforcement Learning with Critic Guidance
    "https://arxiv.org/abs/2605.30161",  # Why Far Looks Up: Probing Spatial Representation in Vision-Language Models
    "https://arxiv.org/abs/2605.30226",  # BORA: Bridging Offline Reinforcement Learning and Online Residual Adaptation for Real-World Dexterous VLA Models
    "https://arxiv.org/abs/2605.30280",  # Qwen-VLA: Unifying Vision-Language-Action Modeling across Tasks, Environments, and Robot Embodiments
    "https://arxiv.org/abs/2605.30290",  # Self-Trained Verification for Training- and Test-Time Self-Improvement
    "https://arxiv.org/abs/2605.30341",  # GPIC: A Giant Permissive Image Corpus for Visual Generation
    "https://arxiv.org/abs/2605.30347",  # NeuROK: Generative 4D Neural Object Kinematics
    "https://arxiv.org/abs/2605.30350",  # DynaFLIP: Rethinking Robotics Perception via Tri-Modal-Dynamics Guided Representation
    "https://arxiv.org/abs/2605.30370",  # Updating the standard neuron model in artificial neural networks
    "https://arxiv.org/abs/2605.30557",  # Seeing Isn't Knowing: Do VLMs Know When Not to Answer Spatial Questions (and Why)?
    "https://arxiv.org/abs/2605.30561",  # VLM3: Vision Language Models Are Native 3D Learners
    "https://arxiv.org/abs/2605.30834",  # Hide-and-Seek in Trajectories: Discovering Failure Signals for VLA Runtime Monitoring
    "https://arxiv.org/abs/2605.31124",  # QVGGT: Post-Training Quantized Visual Geometry Grounded Transformer
    "https://arxiv.org/abs/2605.31159",  # Trust-Region Behavior Blending for On-Policy Distillation
    "https://arxiv.org/abs/2605.31228",  # EchoRL: Reinforcement Learning via Rollout Echoing
    "https://arxiv.org/abs/2605.31604",  # Representation Forcing for Bottleneck-Free Unified Multimodal Models
    "https://arxiv.org/abs/2606.00351",  # UniVerse: A Unified Modulation Framework for Segmentation-Free,Disentangled Multi-Concept Personalization
    "https://arxiv.org/abs/2606.01027",  # $τ_0$-WM: A Unified Video-Action World Model for Robotic Manipulation
    "https://arxiv.org/abs/2606.01851",  # PHASOR: Phase-Anchored Universal Action Representations for Humanoid Embodiments
    "https://arxiv.org/abs/2606.01951",  # Co-training with Ego-centric Video and Demonstration for Robot Navigation Task
    "https://arxiv.org/abs/2606.01955",  # WALL-WM: Carving World Action Modeling at the Event Joints
    "https://arxiv.org/abs/2606.02027",  # World-Task Factorization for Robot Learning
    "https://arxiv.org/abs/2606.02058",  # TIDES: Time-Derivative Event Simulation via Deformable Reconstruction
    "https://arxiv.org/abs/2606.02274",  # Dexterity-BEV: Aligning 3D World and Actions for Generalizable Robot Policies Learning
    "https://arxiv.org/abs/2606.02277",  # RoboSemanticBench: Diagnosing Semantic Grounding in Action Prediction for VLA Models
    "https://arxiv.org/abs/2606.02280",  # Dynamics Are Learned, Not Told: Semi-Supervised Discovery of Latent Dynamics Geometries For Zero-Shot Policy Adaptation
    "https://arxiv.org/abs/2606.02307",  # FATE-VLA:Failue-aware test generation for vision-language-action models
    "https://arxiv.org/abs/2606.02313",  # Towards Precise Intent-Aligned VLA Aerial Navigation via Expert-Guided GRPO
    "https://arxiv.org/abs/2606.02432",  # NDPP-Grasp: Non-Differentiable Physical Plausibility Constraint-Guided Task-Oriented Dexterous Grasp Generation
    "https://arxiv.org/abs/2606.02436",  # Geometry-Aware Implicit Memory for Video World Models
    "https://arxiv.org/abs/2606.02486",  # Intercepting the Future: Latent-Space Predictive World Model for Dynamic VLA Manipulation
    "https://arxiv.org/abs/2606.02551",  # AFUN: Towards an Affordance Foundation Model for Functionality Understanding
    "https://arxiv.org/abs/2606.02577",  # RoboDream: Compositional World Models for Scalable Robot Data Synthesis
    "https://arxiv.org/abs/2606.02735",  # See Less, Specify More: Visual Evidence Budgets for Generalizable VLAs
    "https://arxiv.org/abs/2606.02745",  # SeeTraceAct: Visibility-Aware Latent Planning from Cross-Embodiment Demonstration Videos
    "https://arxiv.org/abs/2606.02767",  # Hybrid Adaptive Kalman Filtering for Data-Efficient Joint Tracking and Classification
    "https://arxiv.org/abs/2606.02800",  # Cosmos 3: Omnimodal World Models for Physical AI
    "https://arxiv.org/abs/2606.03047",  # ModuLoop : Low-Level Code Generation using Modular Synthesizer and Closed-Loop Debugger for Robotic Control
    "https://arxiv.org/abs/2606.03127",  # TTT-VLA: Test-Time Latent Prompt Optimization for Vision-Language-Action Models
    "https://arxiv.org/abs/2606.03159",  # NVIDIA OmniDreams: Real-Time Generative World Model for Closed-Loop Autonomous Vehicle Simulation
    "https://arxiv.org/abs/2606.03188",  # GeoSem-WAM: Geometry- and Semantic-Aware World Action Models
    "https://arxiv.org/abs/2606.03240",  # GeoAlign: Beyond Semantics with State-Guided Spatial Alignment in VLA Models
    "https://arxiv.org/abs/2606.03268",  # EaDex: A Cross-Embodiment Dexterous Manipulation Framework from Low-Cost Demonstrations
    "https://arxiv.org/abs/2606.03296",  # Bridging Predictive Uncertainty and Safe Action: Sample-Conditioned Differentiable Planning for Autonomous Driving
    "https://arxiv.org/abs/2606.03297",  # SplitAdapter: Load-Aware Humanoid Loco-Manipulation via Factorized Adaptation
    "https://arxiv.org/abs/2606.03335",  # GPU-Parallel Multi-Task Reinforcement Learning with Demonstration Guided Policy Optimization
    "https://arxiv.org/abs/2606.03374",  # eMEM: A Hybrid Spatio-Temporal Memory System For Embodied Agents
    "https://arxiv.org/abs/2606.03385",  # Grasp-Then-Plan with Failure Attribution: A Closed Two-Stage Framework for Precise and Generalizable Robotic Manipulation
    "https://arxiv.org/abs/2606.03392",  # OpenEAI-Platform: An Open-source Embodied Artificial Intelligence Hardware-Software Unified Platform
    "https://arxiv.org/abs/2606.03441",  # PerchRL: Vision-Based Agile Perching on Inclined Platforms under Rapid and Irregular Motion
    "https://arxiv.org/abs/2606.03476",  # Human2Humanoid: Physics-Aware Cross-Morphology Motion Retargeting for Humanoid Robots
    "https://arxiv.org/abs/2606.03512",  # SPADE: Sketch-guided Path Planning Augmented with Diffusion Experts
    "https://arxiv.org/abs/2606.03536",  # Bionic Human-Motion Style Transfer for Physically Executable Whole-Body Control of Humanoid Robots
    "https://arxiv.org/abs/2606.03551",  # NVIDIA Isaac Sim: Enabling Scalable, GPU-Accelerated Simulation for Robotics
    "https://arxiv.org/abs/2606.03556",  # Partially Observable Adversarial Patch Attacks on Vision-Language-Action Models in Robotics
    "https://arxiv.org/abs/2606.03598",  # PHASER: Phase-Aware and Semantic Experience Replay for Vision-Language-Action Models
    "https://arxiv.org/abs/2606.03682",  # GN0: Toward a Unified Paradigm for Generation, Evaluation, and Policy Learning in Visual-Language Navigation
    "https://arxiv.org/abs/2606.03784",  # Revisiting Embodied Chain-of-Thought for Generalizable Robot Manipulation
    "https://arxiv.org/abs/2606.03834",  # Let the Dynamics Flow: Stable Flow Matching Dynamical Systems
    "https://arxiv.org/abs/2606.03920",  # Benchmarking Visual State Tracking in Multimodal Video Understanding
    "https://arxiv.org/abs/2606.03937",  # Entropy Is Not Enough: Unlocking Effective Reinforcement Learning for Visual Reasoning via Vision-Anchored Token Selection
    "https://arxiv.org/abs/2606.03940",  # SEAOTTER: Sensor Embedded Autoencoding with One-Time Transcode for Efficient Reconstruction
    "https://arxiv.org/abs/2606.03943",  # PointAction: 3D Points as Universal Action Representations for Robot Control
    "https://arxiv.org/abs/2606.03963",  # Self-Refining Agentic Reinforcement Learning for Vision-Conditioned UAV Navigation
    "https://arxiv.org/abs/2606.03980",  # Skill-RM: Unifying Heterogeneous Evaluation Criteria via Agent Skill
    "https://arxiv.org/abs/2606.03985",  # Humanoid-GPT: Scaling Data and Structure for Zero-Shot Motion Tracking
    "https://arxiv.org/abs/2606.03988",  # Imaginative Perception Tokens Enhance Spatial Reasoning in Multimodal Language Models
    "https://arxiv.org/abs/2606.04130",  # CLAW: Learning Continuous Latent Action World Models via Adversarial Latent Regularization
    "https://arxiv.org/abs/2606.04233",  # What Are We Actually Benchmarking in Robot Manipulation?
    "https://arxiv.org/abs/2606.04269",  # Instant-Fold: In-Context Imitation Learning for Deformable Object Manipulation
    "https://arxiv.org/abs/2606.04433",  # Stateful Visual Encoders for Vision-Language Models
    "https://arxiv.org/abs/2606.04436",  # 3DThinkVLA: Endowing Vision-Language-Action Models with Latent 3D Priors via 3D-Thinking-Guided Co-training
    "https://arxiv.org/abs/2606.04463",  # OSCAR: Omni-Embodiment Skeleton-Conditioned World Action Model for Robotics
    "https://arxiv.org/abs/2606.04708",  # VISTA: Vision-Grounded and Physics-Validated Adaptation of UMI data for VLA Training
    "https://arxiv.org/abs/2606.04718",  # CoRe-MoE: Contrastive Reweighted Mixture of Experts for Multi-Terrain Humanoid Locomotion with Gait Adaptation
    "https://arxiv.org/abs/2606.04811",  # Dream.exe: Can Video Generation Models Dream Executable Robot Manipulation?
    "https://arxiv.org/abs/2606.04825",  # HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning
    "https://arxiv.org/abs/2606.04907",  # WAM-Nav: Asymmetric Latent World-Action Modeling for Unified Visual Navigation
    "https://arxiv.org/abs/2606.04923",  # Reproducing, Analyzing, and Detecting Reward Hacking in Rubric-Based Reinforcement Learning
    "https://arxiv.org/abs/2606.04968",  # Potential-Guided Flow Matching for Vision-Language-Action Policy Improvement
    "https://arxiv.org/abs/2606.05015",  # Generalization of World Models under Environmental Variability for Vision-based Quadrotor Navigation
    "https://arxiv.org/abs/2606.05159",  # X4Val: Learning Neural Surrogates for Variance-Reduced Policy Evaluation
    "https://arxiv.org/abs/2606.05160",  # GRAIL: Generating Humanoid Loco-Manipulation from 3D Assets and Video Priors
    "https://arxiv.org/abs/2606.05254",  # Flash-WAM: Modality-Aware Distillation for World Action Models
    "https://arxiv.org/abs/2606.05328",  # The Invisible Hand of Physics: When Video Diffusion Models Know More Than They Show
    "https://arxiv.org/abs/2606.05395",  # VASO: Formally Verifiable Self-Evolving Skills for Physical AI Agents
    "https://arxiv.org/abs/2606.05468",  # FlowPRO: Reward-Free Reinforced Fine-Tuning of Flow-Matching VLAs via Proximalized Preference Optimization
    "https://arxiv.org/abs/2606.05645",  # Discrete-WAM: Unified Discrete Vision-Action Token Editing for World-Policy Learning
    "https://arxiv.org/abs/2606.05699",  # DexFuture: Hierarchical Future-State Visuomotor Targeting for Bimanual Dexterous Tool Use
    "https://arxiv.org/abs/2606.05737",  # Let It Be Simple: One-Step Action Generation for Vision-Language-Action Models
    "https://arxiv.org/abs/2606.05773",  # PiL-World: A Chunk-Wise World Model for VLA Policy-in-the-Loop Evaluation
    "https://arxiv.org/abs/2606.05873",  # LadderMan: Learning Humanoid Perceptive Ladder Climbing
    "https://arxiv.org/abs/2606.05880",  # TAGA: Terrain-aware Active Gaze Learning for Generalizable Agile Humanoid Locomotion
    "https://arxiv.org/abs/2606.05979",  # World-Language-Action Model for Unified World Modeling, Language Reasoning, and Action Synthesis
    "https://arxiv.org/abs/2606.06041",  # Sample-efficient Low-level Motion Planning for Robotic Manipulation Tasks via Zero-shot Transfer Learning
    "https://arxiv.org/abs/2606.06049",  # L-SDPPO: Policy Optimization of Spiking Diffusion Policy for Intra-vehicular Robotic Manipulation
    "https://arxiv.org/abs/2606.06076",  # Learning Visual Spatial Planning from Symbolic State via Modality-Gap-Aware Self-Distillation
    "https://arxiv.org/abs/2606.06139",  # MotionDisco: Motion Discovery for Extreme Humanoid Loco-Manipulation
    "https://arxiv.org/abs/2606.06194",  # ActiveMimic: Egocentric Video Pretraining with Active Perception
    "https://arxiv.org/abs/2606.06218",  # TAM: Torque Adaptation Module for Robust Motion Transfer in Manipulation
    "https://arxiv.org/abs/2606.06493",  # HANDOFF: Humanoid Agentic Task-Space Whole-Body Control via Distilled Complementary Teachers
    "https://arxiv.org/abs/2606.06556",  # Robots Need More than VLA and World Models
    "https://arxiv.org/abs/2606.06627",  # What Matters When Cotraining Robot Manipulation Policies on Everyday Human Videos?
    "https://arxiv.org/abs/2606.07017",  # The Sim-to-Real Gap of Foundation Model Agents: A Unified MDP Perspective
    "https://arxiv.org/abs/2606.07082",  # On the Geometry of On-Policy Distillation
    "https://arxiv.org/abs/2606.07100",  # LARA: Latent Action Representation Alignment for Vision-Language-Action Models
    "https://arxiv.org/abs/2606.07326",  # AnchorWorld: Embodied Egocentric World Simulation with View-based Evolution Customization
    "https://arxiv.org/abs/2606.07383",  # RhinoVLA Technical Report
    "https://arxiv.org/abs/2606.07500",  # Sparse Subspace-to-Expert Sharing for Task-Agnostic Continual Learning
    "https://arxiv.org/abs/2606.08432",  # Trajectory-Refined Distillation
    "https://arxiv.org/abs/2606.08688",  # PhysAgent: Automating Physics-Based 4D Synthesis via Trajectory-Grounded Multi-Agent Feedback
    "https://arxiv.org/abs/2606.08708",  # PRPO: Perception-Reinforced Policy Optimization via Token-Level Dynamic Advantage Reshaping
    "https://arxiv.org/abs/2606.08737",  # Dream-Tac: A Unified Tactile World Action Model for Contact-Rich Robot Manipulation
    "https://arxiv.org/abs/2606.08775",  # Unifying Object-Centric World Models and Diffusion Policy: A Hierarchical Framework for Multi-Stage Robotic Tasks
    "https://arxiv.org/abs/2606.08828",  # Video2Sim2Real: Full-Stack Autonomous Dexterous Skill Acquisition from a Single Human Video
    "https://arxiv.org/abs/2606.08962",  # C$^3$ache: Accelerating World Action Models with Cross Inference Chunk Cache
    "https://arxiv.org/abs/2606.08992",  # SpaceVLN: A Zero-Shot Vision-and-Language Navigation Agent with Online Spatial Cognitive Memory and Reasoning
    "https://arxiv.org/abs/2606.09215",  # MotionWAM: Towards Foundation World Action Models for Real-Time Humanoid Loco-Manipulation
    "https://arxiv.org/abs/2606.09314",  # KPGrasp: Scalable Keypoint Flow Matching for Dexterous Grasp Generation
    "https://arxiv.org/abs/2606.09337",  # TORL-VLA: Tactile Guided Online Reinforcement Learning for Contact-Rich Manipulation
    "https://arxiv.org/abs/2606.09498",  # Self-Harness: Harnesses That Improve Themselves
    "https://arxiv.org/abs/2606.09499",  # Targeting World Models to Compromise Robot Learning Pipelines
    "https://arxiv.org/abs/2606.09572",  # CT-VAM: A Cerebello-Thalamic-Inspired Vision-Action Model for Efficient Visuomotor Control
    "https://arxiv.org/abs/2606.09615",  # DexPIE: Stable Dexterous Policy Improvement from Real-World Experience
    "https://arxiv.org/abs/2606.09630",  # ReCoVLA: VLM-Guided Reward Compilation for Failure Recovery in Vision-Language-Action Policies
    "https://arxiv.org/abs/2606.09640",  # Physics-Aware Sparse Learning and Selective Online Adaptation for Euler-Lagrange Robot Dynamics
    "https://arxiv.org/abs/2606.09669",  # SpatialWorld: Benchmarking Interactive Spatial Reasoning of Multimodal Agents in Real-World Tasks
    "https://arxiv.org/abs/2606.09740",  # ProbeAct: Probe-Guided Training-Free Failure Recovery in Vision-Language-Action Models
    "https://arxiv.org/abs/2606.09758",  # Difference-Aware Retrieval Policies for Imitation Learning
    "https://arxiv.org/abs/2606.09803",  # Echo-Memory: A Controlled Study of Memory in Action World Models
    "https://arxiv.org/abs/2606.09811",  # AHA-WAM:Asynchronous Horizon-Adaptive World-Action Modeling with Observation-Guided Context Routing
    "https://arxiv.org/abs/2606.09813",  # iMaC: Translating Actions into Motion and Contact Images for Embodied World Models
    "https://arxiv.org/abs/2606.09827",  # MemoryVLA++: Temporal Modeling via Memory and Imagination in Vision-Language-Action Models
    "https://arxiv.org/abs/2606.09828",  # Latent Spatial Memory for Video World Models
    "https://arxiv.org/abs/2606.10025",  # GHOST: Hierarchical Sub-Goal Policies for Generalizing Robot Manipulation
    "https://arxiv.org/abs/2606.10040",  # Efficient-WAM: A 1B-Parameter World-Action Model with Low-Cost Future Imagination
    "https://arxiv.org/abs/2606.10267",  # What Matters in Orchestrating Robot Policies: A Systematic Study of Hierarchical VLA Agents
    "https://arxiv.org/abs/2606.10288",  # MARCH: Model-Assisted Reinforcement Learning for the Perceptive Control of Humanoids over Sparse Footholds
    "https://arxiv.org/abs/2606.10305",  # SARM2: Multi-Task Stage Aware Reward Modeling for Self Improving Robotic Manipulation
    "https://arxiv.org/abs/2606.10340",  # OMG: Omni-Modal Motion Generation for Generalist Humanoid Control
    "https://arxiv.org/abs/2606.10363",  # HiMem-WAM: Hierarchical Memory-Gated World Action Models for Robotic Manipulation
    "https://arxiv.org/abs/2606.10366",  # A Practical Recipe Towards Improving Sim-and-Real Correlation for VLA Evaluation
    "https://arxiv.org/abs/2606.10577",  # AgenticNav: Zero-Shot Vision-and-Language Navigation as a Tool-Calling Harness
    "https://arxiv.org/abs/2606.10614",  # Dexterous Point Policy: Learning Point-based Dexterous Hand Policies from Human Demonstrations
    "https://arxiv.org/abs/2606.10899",  # MV-Actor: Aligning Multi-View Semantics and Spatial Awareness for Bimanual Manipulation
    "https://arxiv.org/abs/2606.11025",  # Flow-DPPO: Divergence Proximal Policy Optimization for Flow Matching Models
    "https://arxiv.org/abs/2606.11087",  # Test-Time Gradient Guidance of Flow Policies in Reinforcement Learning
    "https://arxiv.org/abs/2606.11184",  # TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation
    "https://arxiv.org/abs/2606.11277",  # Least-Action-Guided Diffusion for Physical Extrapolation
    "https://arxiv.org/abs/2606.11482",  # Building Social World Models with Large Language Models
    "https://arxiv.org/abs/2606.11628",  # LUCID: Learning Embodiment-Agnostic Intent Models from Unstructured Human Videos for Scalable Dexterous Robot Skill Acquisition
    "https://arxiv.org/abs/2606.11743",  # TacCoRL: Integrating Tactile Feedback into VLA via Simulation
    "https://arxiv.org/abs/2606.11767",  # Blind Dexterous Grasping via Real2Sim2Real Tactile Policy Learning
    "https://arxiv.org/abs/2606.11901",  # DuoBench: A Reproducible Benchmark for Bimanual Manipulation in Simulation and the Real World
    "https://arxiv.org/abs/2606.12042",  # KinematicRL: A Sim-to-Real Reinforcement Learning Framework For Social Navigation With Kinodynamic Feasibility
    "https://arxiv.org/abs/2606.12105",  # DAM-VLA: Decoupled Asynchronous Multimodal Vision Language Action model
    "https://arxiv.org/abs/2606.12207",  # Intelligent Automation for Embodied Benchmark Construction: Pipelines, Embodiments, Simulators, and Trends
    "https://arxiv.org/abs/2606.12217",  # Making Foresight Actionable: Repurposing Representation Alignment in World Action Models
    "https://arxiv.org/abs/2606.12352",  # CHORUS: Decentralized Multi-Embodiment Collaboration with One VLA Policy
    "https://arxiv.org/abs/2606.12365",  # Ambient Diffusion Policy: Imitation Learning from Suboptimal Data in Robotics
    "https://arxiv.org/abs/2606.12370",  # Breaking Entropy Bounds: Accelerating RL Training via MTP with Rejection Sampling
    "https://arxiv.org/abs/2606.12372",  # UniIntervene: Agentic Intervention for Efficient Real-World Reinforcement Learning
    "https://arxiv.org/abs/2606.12402",  # DIRECT: When and Where Should You Allocate Test-Time Compute in Embodied Planners?
    "https://arxiv.org/abs/2606.12403",  # World Pilot: Steering Vision-Language-Action Models with World-Action Priors
    "https://arxiv.org/abs/2606.12406",  # FACTR 2: Learning External Force Sensing for Commodity Robot Arms Improves Policy Learning
    "https://arxiv.org/abs/2606.12497",  # $μ$VLA: On Recurrent Memory for Partially Observable Manipulation in VLA Models
    "https://arxiv.org/abs/2606.12499",  # Action-Effect Memory Pretraining for Robot Manipulation
    "https://arxiv.org/abs/2606.12604",  # EgoEngine: From Egocentric Human Videos to High-Fidelity Dexterous Robot Demonstrations
    "https://arxiv.org/abs/2606.12683",  # From AGI to ASI
    "https://arxiv.org/abs/2606.12690",  # EWAM: An Enhanced World Action Model for Closed-Loop Online Adaptation in Embodied Intelligence
    "https://arxiv.org/abs/2606.12759",  # Sparse2Act: Learning Action-Aligned Sparse 3D Representations for Cross-Domain Robot Manipulation
    "https://arxiv.org/abs/2606.12814",  # Stubborn: A Streamlined and Unified Reinforcement Learning Framework for Robust Motion Tracking and Fall Recovery for Humanoids
    "https://arxiv.org/abs/2606.12956",  # SERF: Spatiotemporal Environment and Robot Feature Map for Long-Horizon Mobile Manipulation
    "https://arxiv.org/abs/2606.12965",  # EmbodiSteer: Steering Embodiment-Agnostic Visuomotor Policies with Joint-Space Guidance for Zero-Shot Cross-Embodiment Deployment
    "https://arxiv.org/abs/2606.13040",  # RoboProcessBench: Benchmarking Process-Aware Understanding in Vision-Language Robotic Manipulation
    "https://arxiv.org/abs/2606.13049",  # Y-BotFrame: An Extensible Embodied Agent Framework for Quadruped Robot Assistants
    "https://arxiv.org/abs/2606.13102",  # FTP-1: A Generalist Foundation Tactile Policy Across Tactile Sensors for Contact-Rich Manipulation
    "https://arxiv.org/abs/2606.13222",  # Proprioceptive-visual correspondence enables self-other distinction in humanoid robots
    "https://arxiv.org/abs/2606.13232",  # WT-UMI: Tactile-based Whole-Body Manipulation via Force-Supervised Contact-Aware Planning
    "https://arxiv.org/abs/2606.13279",  # See Selectively, Act Adaptively: Dual-Level Structural Decomposition for Bimanual Robot Manipulation
    "https://arxiv.org/abs/2606.13400",  # PolyFlow: Safe and Efficient Polytope-Constrained Flow Matching with Constraint Embedding and Projection-free Update
    "https://arxiv.org/abs/2606.13435",  # GIVE: Grounding Human Gestures in Vision-Language-Action Models
    "https://arxiv.org/abs/2606.13494",  # NavWAM: A Navigation World Action Model for Goal-Conditioned Visual Navigation
    "https://arxiv.org/abs/2606.13497",  # SPARC: Reliable Spatial Annotations from Robot Demonstrations at Scale
    "https://arxiv.org/abs/2606.13515",  # MaskWAM: Unifying Mask Prompting and Prediction for World-Action Models
    "https://arxiv.org/abs/2606.13672",  # $\texttt{WEAVER}$, Better, Faster, Longer: An Effective World Model for Robotic Manipulation
    "https://arxiv.org/abs/2606.13675",  # Improving Robotic Generalist Policies via Flow Reversal Steering
    "https://arxiv.org/abs/2606.13677",  # Mana: Dexterous Manipulation of Articulated Tools
    "https://arxiv.org/abs/2606.13769",  # $μ_0$: A Scalable 3D Interaction-Trace World Model
    "https://arxiv.org/abs/2606.13877",  # ContactWorld: What Matters in Vision-Tactile World Models for Contact-Rich Manipulation
    "https://arxiv.org/abs/2606.13886",  # PhysVLA: Towards Physically-Grounded VLA for Embodied Robotic Manipulation
    "https://arxiv.org/abs/2606.14048",  # WAM4D: Fast 4D World Action Model via Spatial Register Tokens
    "https://arxiv.org/abs/2606.14084",  # Self-Improving VLA Policies: Selected Diffusion Noise for Spurious-Robust Action Smoothing
    "https://arxiv.org/abs/2606.14218",  # Universal Manipulation Exoskeleton: Learning Compliant Whole-body Policies with Real-time Torque Feedback
    "https://arxiv.org/abs/2606.14409",  # Hy-Embodied-0.5-VLA: From Vision-Language-Action Models to a Real-World Robot Learning Stack
    "https://arxiv.org/abs/2606.14418",  # Causal Object-Centric Models for Planning with Monte Carlo Tree Search
    "https://arxiv.org/abs/2606.14535",  # Spatially Conditioned Diffusion Policy: Learning Precise and Robust Manipulation with a Single RGB Camera
    "https://arxiv.org/abs/2606.14665",  # EgoGuide: Egocentric Guidance for Efficient Robot-Free Demonstration Collection and Learning
    "https://arxiv.org/abs/2606.15232",  # Rethinking Implicit Spatial Representation in Visuomotor Policy Learning
    "https://arxiv.org/abs/2606.15338",  # SimWeaver: Zero-Shot RGB Sim-to-Real for Deformable Manipulation
    "https://arxiv.org/abs/2606.15654",  # PO-PDDL: Learning Symbolic POMDPs from Visual Demonstrations for Robot Planning Under Uncertainty
    "https://arxiv.org/abs/2606.15685",  # Learning New Tasks via Reusable Skills: Skill-Compositional Experts for Embodied Continual Learning
    "https://arxiv.org/abs/2606.15768",  # LaWAM: Latent World Action Models for Efficient Dynamics-Aware Robot Policies
    "https://arxiv.org/abs/2606.15846",  # FlashNav: Ultra-Fast Policy Training for Robot Navigation within 20 Seconds
    "https://arxiv.org/abs/2606.16202",  # EgoPhys: Learning Generalizable Physics Models of Deformable Objects from Egocentric Video
    "https://arxiv.org/abs/2606.16222",  # Latent Thought Flow: Efficient Latent Reasoning in Large Language Models
    "https://arxiv.org/abs/2606.16272",  # TopoRetarget: Interaction-Preserving Retargeting for Dexterous Manipulation
    "https://arxiv.org/abs/2606.16286",  # FlowMPC: Improving Flow Matching policies with World Models
    "https://arxiv.org/abs/2606.16436",  # V2P-Manip: Learning Dexterous Manipulation from Monocular Human Videos
    "https://arxiv.org/abs/2606.16480",  # HOLO-MPPI: Multi-Scenario Motion Planning via Hierarchical Policy Optimization
    "https://arxiv.org/abs/2606.16519",  # BadWorld: Adversarial Attacks on World Models
    "https://arxiv.org/abs/2606.16542",  # ADAPT: Analytical Disturbance-Aware Policy Training for Humanoid Locomotion
    "https://arxiv.org/abs/2606.16569",  # PROSE: Training-Free Egocentric Scene Registration with Vision-Language Models
    "https://arxiv.org/abs/2606.16690",  # PATCH: Action-Chunk-Conditioned Latent Patch Innovation Monitoring for Robot Manipulation
    "https://arxiv.org/abs/2606.16696",  # VENOM: Versatile Embodied Network for Omni-bodied Motion tracking
    "https://arxiv.org/abs/2606.16826",  # ATOM-Bench: A Real-World Benchmark for Atomic Skills and Compositional Generalization in Manipulation Policies
    "https://arxiv.org/abs/2606.16856",  # Video-Based Optimal Transport for Feedback-Efficient Offline Preference-Based Reinforcement Learning
    "https://arxiv.org/abs/2606.16888",  # LOPAL: Local Performance-Aware Active Learning from Imperfect Demonstrations
    "https://arxiv.org/abs/2606.16917",  # Unified Motion-Action Modeling for Heterogeneous Robot Learning
    "https://arxiv.org/abs/2606.16993",  # DreamX-World 1.0: A General-Purpose Interactive World Model
    "https://arxiv.org/abs/2606.17024",  # ExpRL: Exploratory RL for LLM Mid-Training
    "https://arxiv.org/abs/2606.17040",  # R2RDreamer: 3D-aware Data Augmentation for Spatially-generalized 2D Manipulation Policies
    "https://arxiv.org/abs/2606.17043",  # Hierarchical Advantage Weighting for Online RL Fine-Tuning of VLAs from Sparse Episode Outcomes
    "https://arxiv.org/abs/2606.17046",  # Geometric Action Model for Robot Policy Learning
    "https://arxiv.org/abs/2606.17054",  # Human Universal Grasping
    "https://arxiv.org/abs/2606.17055",  # T-Rex: Tactile-Reactive Dexterous Manipulation
    "https://arxiv.org/abs/2606.17200",  # ACE-Ego-0: Unifying Egocentric Human and Robotic Data for VLA Pretraining
    "https://arxiv.org/abs/2606.17317",  # Transformer-Based Warm-Starting for Feasible and Optimal Terminal Approach to Tumbling Objects with Space Manipulators
    "https://arxiv.org/abs/2606.17385",  # EgoInfinity: A Web-Scale 4D Hand-Object Interaction Data Engine for Any-View Robot Retargeting and Video-to-Action Robot Learning
    "https://arxiv.org/abs/2606.17408",  # Where Should Action Generation Begin? A Learnable Source Prior for Generative Robot Policies
    "https://arxiv.org/abs/2606.17418",  # DexLink Hand: A Compact, Affordable, 16-DOF Linkage-Driven Hand with Human-Like Dexterity
    "https://arxiv.org/abs/2606.17463",  # WeaveLA: Event Driven Cross-Subtask Latent Memory Weaving for Repetitive Robot Manipulation
    "https://arxiv.org/abs/2606.17480",  # GeneralVLA-2: Geometry-Aware Reconstruction and Governed Memory for Robot Planning
    "https://arxiv.org/abs/2606.17493",  # When Robots Sleep: Offline Skill Consolidation for Shared-Policy Robot Learning
    "https://arxiv.org/abs/2606.17520",  # GASE: Gaussian Splatting-Based Automated System for Reconstructing Embodied-Simulation Environments
    "https://arxiv.org/abs/2606.17598",  # MuseVLA: An Adaptive Multimodal Sensing Vision-Language-Action Model for Robotic Manipulation
    "https://arxiv.org/abs/2606.17639",  # ERQA-Plus: A Diagnostic Benchmark for Reasoning in Embodied AI
    "https://arxiv.org/abs/2606.17833",  # HumanoidArena: Benchmarking Egocentric Hierarchical Whole-body Learning
    "https://arxiv.org/abs/2606.17846",  # Qwen-RobotManip Technical Report: Alignment Unlocks Scale for Robotic Manipulation Foundation Models
    "https://arxiv.org/abs/2606.17906",  # WAM-RL: World-Action Model Reinforcement Learning with Reconstruction Rewards and Online Video SFT
    "https://arxiv.org/abs/2606.17924",  # PearlVLA: Progressive Embodied Action-Plan Refinement in Latent Space
    "https://arxiv.org/abs/2606.17937",  # ThinkingVLA: Interleaved Vision and Language Reasoning for Robotic Manipulation
    "https://arxiv.org/abs/2606.17982",  # LAGO Policy: Latency-Aware Asynchronous Diffusion Policies with Goal-Directed Collision-Free Planning for Smooth Manipulation
    "https://arxiv.org/abs/2606.18043",  # Uncertainty Quantification for Flow-Based Vision-Language-Action Models
    "https://arxiv.org/abs/2606.18092",  # EAGG: Embodiment-Aligned Grasp Generation via Geometry-Aware Graph Conditioning
    "https://arxiv.org/abs/2606.18097",  # WireCraft: A Simulation Benchmark for Industrial DLO Manipulation
    "https://arxiv.org/abs/2606.18112",  # Qwen-RobotNav Technical Report: A Scalable Navigation Model Designed for an Agentic Navigation System
    "https://arxiv.org/abs/2606.18189",  # Beyond Failure Recovery: An Engagement-Aware Human-in-the-loop Framework for Robotic Systems
    "https://arxiv.org/abs/2606.18208",  # Looped World Models
    "https://arxiv.org/abs/2606.18239",  # EBench: Elemental Diagnosis of Generalist Mobile Manipulation Policies
    "https://arxiv.org/abs/2606.18243",  # MOCHI: Motion Enhancement of Collaborative Human-object Interactions
    "https://arxiv.org/abs/2606.18247",  # Visual Verification Enables Inference-time Steering and Autonomous Policy Improvement
    "https://arxiv.org/abs/2606.18363",  # Guava: An Effective and Universal Harness for Embodied Manipulation
    "https://arxiv.org/abs/2606.18589",  # DREAM-Chunk: Reactive Action Chunking with Latent World Model
    "https://arxiv.org/abs/2606.18594",  # Benchmarking Action Spaces in Reinforcement Learning for Vision-based Robotic Manipulation
    "https://arxiv.org/abs/2606.18772",  # HALOMI: Learning Humanoid Loco-Manipulation with Active Perception from Human Demonstrations
    "https://arxiv.org/abs/2606.18953",  # Object-Centric Residual RL for Zero-Shot Sim-to-Real VLA Enhancement
    "https://arxiv.org/abs/2606.18959",  # TactSpace: Learning a Physics-enriched Shared Latent Space for Tactile Sim-to-Real Transfer
    "https://arxiv.org/abs/2606.19161",  # HT-Bench: Benchmarking and Learning Dexterous Full-Hand Tactile Representations with Egocentric Vision
    "https://arxiv.org/abs/2606.19194",  # Invertible Neural Network Adapter for One-Step Flow Matching in Robot Manipulation
    "https://arxiv.org/abs/2606.19333",  # Do as I Do: Dexterous Manipulation Data from Everyday Human Videos
]
