#include <iostream>
#include <cstdlib>
#include <iomanip>

class Tabuleiro{
	int pos[4][4];
   public:
	void add();
   public:
	Tabuleiro();
	void move(int);//Movimento do usuário no tabuleiro, recebendo 0 = cima, 1 = baixo, 2 = esquerda, 3 = direita
	void print();//mostra na tela o tabuleiro

};


Tabuleiro::Tabuleiro(){
	for(int i=0;i<4;i++){
		for(int j=0;j<4;j++){
			this->pos[i][j] = 0;
		}
	}
}
void Tabuleiro::add(){
	int x, y, v;
	do{
		x = rand() % 4;
		y = rand() % 4;

	}while(this->pos[x][y] != 0);
	this->pos[x][y] = 2;
}

void Tabuleiro::print(){
	for(int i=0;i<4;i++){
		for(int j=0;j<4;j++){
			std::cout<<std::setw(4)<<this->pos[i][j]<<"|";
		}
		std::cout<<std::endl;
	}
}
void Tabuleiro::move(int dir){
	switch(dir){
		case 0://cima
			for(int i = 1;i < 4; i++){
				for(int j = 0; j < 4; j++){
					int x = 1;
					while(this->pos[i-x][j] == 0 && x < 4){
						this->pos[i-x][j] = this->pos[i-x+1][j];
						this->pos[i-x+1][j] = 0;
						x++;
					}

				}
			}
			break;
		case 1://baixo
			for(int i = 3;i > 0; i--){
                                for(int j = 0; j < 4; j++){
                                        int x = 1;
                                        while(this->pos[i+x][j] == 0 && x < 4){
                                                this->pos[i+x][j] = this->pos[i+x-1][j];
                                                this->pos[i+x-1][j] = 0;
                                                x++;
                                        }

                                }
                        }

			break;
		case 2://esquerda
			for(int j = 1;j < 4; j++){
                                for(int i = 0; i < 4; i++){
                                        int x = 1;
                                        while(this->pos[i][j-x] == 0 && x < 4){
                                                this->pos[i][j-x] = this->pos[i][j-x+1];
                                                this->pos[i][j-x+1] = 0;
                                                x++;
                                        }

                                }
                        }

			break;
		case 3://direita
			for(int j = 3;j > 0; j--){
                                for(int i = 0; i < 4; i++){
                                        int x = 1;
                                        while(this->pos[i][j+x] == 0 && x < 4){
                                                this->pos[i][j+x] = this->pos[i][j+x-1];
                                                this->pos[i][j+x-1] = 0;
                                                x++;
                                        }

                                }
                        }

			break;
	}
}

int main(){
	Tabuleiro a;
	a.add();
	a.add();
	a.add();
	a.add();
	a.add();
	a.print();
	std::cin.get();
	system("clear");
	a.move(3);
	a.print();

	return 0;
}
