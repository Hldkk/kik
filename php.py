import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self, master):
        # Inicjalizacja gry i ustawienie podstawowych parametrów
        self.master = master
        self.master.title("Kółko-krzyżyk")
        
        self.playing_with_computer = False  # Zmienna do określenia trybu gry
        self.current_player = "X"  # Aktualny gracz
        self.computer_player = "O"  # Gracz komputer
        self.difficulty = "hard"  # Ustalenie domyślnego poziomu trudności
        self.players_scores = {"X": 0, "O": 0}  # Słownik do przechowywania wyniku graczy

        self.create_start_menu()  # Utworzenie menu startowego

    def create_start_menu(self):
        """Tworzy menu startowe do wyboru trybu gry."""
        self.start_frame = tk.Frame(self.master)
        self.start_frame.pack()

        self.label = tk.Label(self.start_frame, text="Wybierz tryb gry:", font=("Arial", 16))
        self.label.pack()

        # Przycisk do gry dla dwóch graczy
        self.player_button = tk.Button(self.start_frame, text="Dwóch graczy", command=self.start_two_player_game)
        self.player_button.pack(pady=5)

        # Przycisk do gry z komputerem
        self.computer_button = tk.Button(self.start_frame, text="Graj z komputerem", command=self.select_difficulty)
        self.computer_button.pack(pady=5)

    def select_difficulty(self):
        """Wybiera poziom trudności dla gry z komputerem."""
        self.start_frame.destroy()  # Usuwa menu startowe
        self.difficulty_frame = tk.Frame(self.master)
        self.difficulty_frame.pack()

        self.label = tk.Label(self.difficulty_frame, text="Wybierz poziom trudności:", font=("Arial", 16))
        self.label.pack()

        # Przycisk do wyboru łatwego poziomu
        self.easy_button = tk.Button(self.difficulty_frame, text="Łatwy", command=lambda: self.start_computer_game("easy"))
        self.easy_button.pack(pady=5)

        # Przycisk do wyboru trudnego poziomu
        self.hard_button = tk.Button(self.difficulty_frame, text="Trudny", command=lambda: self.start_computer_game("hard"))
        self.hard_button.pack(pady=5)

    def start_two_player_game(self):
        """Rozpoczyna grę dla dwóch graczy."""
        self.playing_with_computer = False  # Ustala tryb dwóch graczy
        self.start_frame.destroy()  # Usuwa menu startowe
        self.create_game_board()  # Tworzy planszę do gry

    def start_computer_game(self, difficulty):
        """Rozpoczyna grę z komputerem."""
        self.playing_with_computer = True  # Ustala tryb gry z komputerem
        self.difficulty = difficulty  # Zapisuje wybrany poziom trudności
        self.difficulty_frame.destroy()  # Usuwa menu wyboru trudności
        self.create_game_board()  # Tworzy planszę do gry

    def create_game_board(self):
        """Tworzy planszę do gry."""
        self.board = [[" " for _ in range(3)] for _ in range(3)]  # Inicjalizacja pustej planszy
        self.buttons = [[None for _ in range(3)] for _ in range(3)]  # Lista przycisków

        for row in range(3):
            for col in range(3):
                # Tworzenie przycisku dla każdej komórki planszy
                button = tk.Button(self.master, text=" ", font=("Arial", 24), width=5, height=2,
                                   command=lambda r=row, c=col: self.make_move(r, c))
                button.grid(row=row, column=col)  # Ustawienie przycisku na pozycji
                self.buttons[row][col] = button  # Dodanie przycisku do listy

    def make_move(self, row, col):
        """Realizuje ruch gracza."""
        if self.board[row][col] == " ":  # Sprawdzenie, czy komórka jest pusta
            self.board[row][col] = self.current_player  # Aktualizuje planszę
            self.buttons[row][col].config(text=self.current_player)  # Aktualizuje tekst na przycisku

            # Sprawdzenie na zwycięzcę
            if self.check_winner():
                self.players_scores[self.current_player] += 1  # Aktualizuje wynik zwycięzcy
                messagebox.showinfo("Zwycięstwo!", f"Gracz {self.current_player} wygrał!\nWynik: X: {self.players_scores['X']} O: {self.players_scores['O']}")
                self.reset_game()  # Resetuje grę
            elif self.is_board_full():
                messagebox.showinfo("Remis!", "Gra zakończyła się remisem!")  # Powiadomienie o remisie
                self.reset_game()  # Resetuje grę
            else:
                if self.playing_with_computer and self.current_player == "X":
                    self.current_player = self.computer_player  # Zmiana ruchu na komputer
                    self.computer_move()  # Wykonanie ruchu komputera
                elif not self.playing_with_computer:
                    self.current_player = "X" if self.current_player == "O" else "O"  # Zmiana gracza

    def computer_move(self):
        """Wykonuje ruch komputera."""
        if self.difficulty == "hard":
            best_score = float('-inf')  # Inicjalizacja najlepszego wyniku
            best_move = None  # Najlepszy ruch
            for row in range(3):
                for col in range(3):
                    if self.board[row][col] == " ":  # Sprawdzenie na pustą komórkę
                        self.board[row][col] = self.computer_player  # Symuluje ruch komputera
                        score = self.minimax(self.board, False)  # Ocena ruchu
                        self.board[row][col] = " "  # Resetuje zmiany
                        if score > best_score:  # Aktualizuje najlepszy wynik
                            best_score = score
                            best_move = (row, col)  # Zapamiętuje najlepszy ruch

            if best_move:
                self.board[best_move[0]][best_move[1]] = self.computer_player  # Wykonuje najlepszy ruch
                self.buttons[best_move[0]][best_move[1]].config(text=self.computer_player)  # Aktualizuje przycisk
        else:  # Łatwy poziom
            empty_cells = [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == " "]  # Znajduje puste komórki
            if empty_cells:
                row, col = random.choice(empty_cells)  # Losowy wybór komórki
                self.board[row][col] = self.computer_player  # Wykonanie ruchu komputera
                self.buttons[row][col].config(text=self.computer_player)  # Aktualizuje przycisk

        # Sprawdzenie na zwycięzcę
        if self.check_winner():
            messagebox.showinfo("Zwycięstwo!", f"Komputer wygrał!\nWynik: X: {self.players_scores['X']} O: {self.players_scores['O']}")
            self.reset_game()  # Resetuje grę
        elif self.is_board_full():
            messagebox.showinfo("Remis!", "Gra zakończyła się remisem!")  # Powiadomienie o remisie
            self.reset_game()  # Resetuje grę
        else:
            self.current_player = "X"  # Zmiana ruchu na gracza X

    def minimax(self, board, is_maximizing):
        """Algorytm minimax do wyboru najlepszego ruchu komputera."""
        winner = self.check_winner()  # Sprawdzenie na zwycięzcę
        if winner == self.computer_player:
            return 1  # Wynik dla zwycięstwa komputera
        elif winner == "X":
            return -1  # Wynik dla zwycięstwa gracza X
        elif self.is_board_full():
            return 0  # Remis

        if is_maximizing:  # Jeśli komputer maksymalizuje wynik
            best_score = float('-inf')  # Inicjalizacja najlepszego wyniku
            for row in range(3):
                for col in range(3):
                    if board[row][col] == " ":  # Sprawdzenie na pustą komórkę
                        board[row][col] = self.computer_player  # Symuluje ruch komputera
                        score = self.minimax(board, False)  # Ocena ruchu
                        board[row][col] = " "  # Resetuje zmiany
                        best_score = max(score, best_score)  # Aktualizuje najlepszy wynik
            return best_score
        else:  # Jeśli gracz minimalizuje wynik
            best_score = float('inf')  # Inicjalizacja najgorszego wyniku
            for row in range(3):
                for col in range(3):
                    if board[row][col] == " ":  # Sprawdzenie na pustą komórkę
                        board[row][col] = "X"  # Symuluje ruch gracza
                        score = self.minimax(board, True)  # Ocena ruchu
                        board[row][col] = " "  # Resetuje zmiany
                        best_score = min(score, best_score)  # Aktualizuje najgorszy wynik
            return best_score

    def check_winner(self):
        """Sprawdza, czy jest zwycięzca."""
        for row in self.board:
            if row.count(row[0]) == len(row) and row[0] != " ":  # Sprawdzenie wierszy
                return row[0]  # Zwraca zwycięzcę

        for col in range(3):
            if all(self.board[row][col] == self.board[0][col] and self.board[0][col] != " " for row in range(3)):  # Sprawdzenie kolumn
                return self.board[0][col]  # Zwraca zwycięzcę

        if all(self.board[i][i] == self.board[0][0] and self.board[0][0] != " " for i in range(3)):  # Sprawdzenie głównej przekątnej
            return self.board[0][0]  # Zwraca zwycięzcę

        if all(self.board[i][2 - i] == self.board[0][2] and self.board[0][2] != " " for i in range(3)):  # Sprawdzenie drugiej przekątnej
            return self.board[0][2]  # Zwraca zwycięzcę

        return None  # Jeśli nie ma zwycięzcy

    def is_board_full(self):
        """Sprawdza, czy plansza jest pełna."""
        return all(cell != " " for row in self.board for cell in row)  # Zwraca True, jeśli wszystkie komórki są pełne

    def reset_game(self):
        """Resetuje grę do początkowego stanu."""
        self.board = [[" " for _ in range(3)] for _ in range(3)]  # Inicjalizacja nowej planszy
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(text=" ")  # Oczyszcza tekst na przyciskach
        self.current_player = "X"  # Ustala, że gracz zaczyna od X

if __name__ == "__main__":
    root = tk.Tk()  # Tworzy główne okno
    game = TicTacToe(root)  # Inicjalizacja gry
    root.mainloop()  # Uruchamia główną pętlę
