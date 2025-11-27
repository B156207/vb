from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
import numpy as np


def create_oracle(secret_string):
    n = len(secret_string)
    oracle = QuantumCircuit(n + 1, name='Oracle')
    for i, bit in enumerate(reversed(secret_string)):
        if bit == '1':
            oracle.cx(i, n)
    
    return oracle


def bernstein_vazirani_circuit(secret_string):
    n = len(secret_string)
    
    qr = QuantumRegister(n, 'q')
    auxiliary = QuantumRegister(1, 'aux')
    cr = ClassicalRegister(n, 'c')
    
    circuit = QuantumCircuit(qr, auxiliary, cr)
    
    circuit.x(auxiliary[0])
    circuit.h(auxiliary[0])

    circuit.h(qr)
    
    circuit.barrier()
    
    oracle = create_oracle(secret_string)
    circuit.compose(oracle, qubits=list(range(n + 1)), inplace=True)
    
    circuit.barrier()
    
    circuit.h(qr)
    
    circuit.measure(qr, cr)
    
    return circuit


def simulate_circuit(circuit, shots=1024):
    simulator = AerSimulator()
    job = simulator.run(circuit, shots=shots)
    result = job.result()
    counts = result.get_counts()
    
    return counts


def validate_binary_string(s):
    return all(c in '01' for c in s) and len(s) > 0


def display_circuit_info(secret_string, circuit):
    print("\n" + "="*70)
    print("CIRCUIT INFORMATION")
    print("="*70)
    print(f"Number of qubits: {circuit.num_qubits}")
    print(f"Number of classical bits: {circuit.num_clbits}")
    print(f"Circuit depth: {circuit.depth()}")
    print(f"Secret string length: {len(secret_string)} bits")
    print("="*70)


def run_bernstein_vazirani(secret_string, show_circuit=True, shots=1024):
    print("\n" + "="*70)
    print("BERNSTEIN-VAZIRANI ALGORITHM")
    print("="*70)
    print(f"Secret string (hidden): {secret_string}")
    print(f"Length: {len(secret_string)} bits")
    print("="*70)
    
    print("\n[1] Building quantum circuit...")
    circuit = bernstein_vazirani_circuit(secret_string)
    
    display_circuit_info(secret_string, circuit)
    
    if show_circuit:
        print("\n[2] Circuit Diagram:")
        print("-" * 70)
        print(circuit.draw(output='text', fold=-1))
        print("-" * 70)
    
    print(f"\n[3] Running quantum simulation with {shots} shots...")
    counts = simulate_circuit(circuit, shots=shots)
    
    print("\n" + "="*70)
    print("MEASUREMENT RESULTS")
    print("="*70)
    
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    
    for measured_string, count in sorted_counts:
        percentage = (count / shots) * 100
        bar = '█' * int(percentage / 2)
        print(f"{measured_string}: {count:4d} ({percentage:6.2f}%) {bar}")
    
    found_string = max(counts, key=counts.get)
    
    print("="*70)
    print("\n" + "="*70)
    print("ALGORITHM RESULT")
    print("="*70)
    print(f"Found string:  {found_string}")
    print(f"Secret string: {secret_string}")
    
    if found_string == secret_string:
        print("\n✓ SUCCESS! The algorithm correctly found the secret string!")
    else:
        print("\n✗ MISMATCH! This shouldn't happen in ideal conditions.")
    
    print("="*70)
    
    print("\n" + "="*70)
    print("QUANTUM ADVANTAGE")
    print("="*70)
    print(f"Quantum queries needed:  1")
    print(f"Classical queries needed: {len(secret_string)} (in worst case)")
    print(f"Speedup factor: {len(secret_string)}x")
    print("="*70 + "\n")


def interactive_mode():
    print("\n" + "="*70)
    print("BERNSTEIN-VAZIRANI ALGORITHM - INTERACTIVE MODE")
    print("="*70)
    print("\nThis algorithm can find a hidden binary string in just ONE query!")
    print("Classical algorithms would need multiple queries (one per bit).\n")
    
    while True:
        print("\nOptions:")
        print("1. Enter custom secret string")
        print("2. Use random secret string")
        print("3. Run demo with example strings")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            secret = input("\nEnter binary string (e.g., '101010'): ").strip()
            if not validate_binary_string(secret):
                print("❌ Error: String must contain only 0s and 1s!")
                continue
            
            show = input("Show circuit diagram? (y/n): ").strip().lower() == 'y'
            shots = input("Number of shots (default 1024): ").strip()
            shots = int(shots) if shots.isdigit() else 1024
            
            run_bernstein_vazirani(secret, show_circuit=show, shots=shots)
            
        elif choice == '2':
            length = input("\nEnter string length (default 6): ").strip()
            length = int(length) if length.isdigit() and int(length) > 0 else 6
            
            secret = ''.join(np.random.choice(['0', '1']) for _ in range(length))
            
            show = input("Show circuit diagram? (y/n): ").strip().lower() == 'y'
            shots = input("Number of shots (default 1024): ").strip()
            shots = int(shots) if shots.isdigit() else 1024
            
            run_bernstein_vazirani(secret, show_circuit=show, shots=shots)
            
        elif choice == '3':
            print("\nRunning demos with example strings...\n")
            examples = ['101', '1111', '10101010', '11001100']
            
            for secret in examples:
                input(f"\nPress Enter to run with secret string '{secret}'...")
                run_bernstein_vazirani(secret, show_circuit=False, shots=1024)
            
        elif choice == '4':
            print("\nThank you for using the Bernstein-Vazirani Algorithm!")
            print("="*70 + "\n")
            break
            
        else:
            print("❌ Invalid choice! Please enter 1-4.")


def main():
    print("\n" + "="*70)
    print(" " * 15 + "BERNSTEIN-VAZIRANI ALGORITHM")
    print(" " * 20 + "Quantum Computing Demo")
    print("="*70)
    
    try:
        interactive_mode()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user.")
        print("="*70 + "\n")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("="*70 + "\n")


if __name__ == "__main__":
    main()
