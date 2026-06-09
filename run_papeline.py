import subprocess

scripts = [
    "genome_summary.py",
    "gc_content.py",
    "compare_genome.py",
    "VCF_to_table.py",
    "mutation_map.py"
]

for script in scripts:
    print(f"\nRunning {script}...")
    subprocess.run(["python", script], check=True)

print("\nPipeline finished successfully!")
