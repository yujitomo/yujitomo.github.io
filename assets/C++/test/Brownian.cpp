#include <iostream>
#include <string>
#include <cstdlib>
#include <cmath>
#include <random>

using namespace std;


double normal_dist_func_N(double x) {
    return 0.5*(1 + (x - 2*pow(x,3)/3 + 2*pow(x,5)/5 - 4*pow(x,7)/21 + 2*pow(x,9)/27 - 4*pow(x,11)/165 + 4*pow(x,13)/585)*sqrt(2)/sqrt(3.141592653589793238462643));
    // return 0.5*(1 + erf(x / sqrt(2)));
}

double EuroAnalytic(string PutOrCall,
                    double Expiry,  // 権利行使価格K
                    double Strike,  // 満期T
                    double Spot,  // 現時点t=0での原資産価格S_0
                    double Vol,  // ボラティリティσ
                    double DivYld, // 配当利回り
                    double r  // 金利r
) {
    double logTerm = log( Spot / Strike );
    double thisD1 = ( logTerm + ( r - DivYld + 0.5*Vol*Vol)*Expiry ) / Vol*sqrt(Expiry);
    double thisD2 = thisD1 - Vol*sqrt(Expiry);
    double firstTerm;
    double secondTerm;

    if ( PutOrCall == "C" ) {
        firstTerm = Spot*exp(-DivYld*Expiry)*normal_dist_func_N(thisD1);
        secondTerm = Strike*exp(-r*Expiry)*normal_dist_func_N(thisD2);
    } else if ( PutOrCall == "P" ) {
        firstTerm = - Spot*exp(-DivYld*Expiry)*normal_dist_func_N(-thisD1);
        secondTerm = - Strike*exp(-r*Expiry)*normal_dist_func_N(-thisD2);
    }
    return firstTerm - secondTerm;
}


double EuroMonteCarlo(string PutOrCall,  // putかcallか
                      double Expiry,  // 満期T
                      double Strike,  // 権利行使価格K
                      double Spot,  // 現時点t=0での原資産価格S_0
                      double Vol,  // ボラティリティσ
                      double DivYld, // 配当利回り
                      double r,  // 金利r
                      unsigned long NumberOfPaths) {
    double Variance = Vol*Vol*Expiry;  // 分散
    double ItoCorrection = -0.5*Variance;  // -σ^2T/2

    double RootExpiry = sqrt(Expiry);  // √T

    random_device seed_gen;
    mt19937 generator(seed_gen());
    // default_random_engine generator(seed_gen());
    normal_distribution<double> Wiener(0,RootExpiry);  // W_Tの分布はN(0,T)

    double movedSpot = Spot*exp((r - DivYld)*Expiry - 0.5*Vol*Vol*Expiry);  // S_0exp(T(r-σ^2/2))
    double thisSpot;
    double runningSum=0;

    for (unsigned long i=0; i < NumberOfPaths; i++) {
        double thisGaussian = Wiener(generator);
        thisSpot = movedSpot*exp(Vol*thisGaussian);  // S_0exp(σ*W_T + T(r-σ^2/2))
        double thisPayoff = thisSpot - Strike;
        if ( PutOrCall == "C" ) {
            thisPayoff *= 1;
        } else if ( PutOrCall == "P" ) {
            thisPayoff *= -1;
        }
        thisPayoff = thisPayoff > 0 ? thisPayoff : 0;
        runningSum += thisPayoff;
    }

    double mean = runningSum / NumberOfPaths;
    mean *= exp(-(r - DivYld)*Expiry);  // 求めたいのはexp(-rT)E[S_0exp(σ*W_T + T(r-σ^2/2))]なので現在価値に換算
    return mean;
}



int main()
{
    string PutOrCall;
    double Expiry;
    double Strike;
    double Spot;
    double Vol;
    double DivYld;
    double r;
    unsigned long NumberOfPaths;

    cout << "\nPut or Call\n";
    cin >> PutOrCall;

    if ( PutOrCall == "default" ) {
        Expiry = 0.084;
        Strike = 15500;
        Spot = 15000;
        Vol = 0.2;
        DivYld = 0.015;
        r = 0.0015;
        NumberOfPaths = 10000000;
        cout << "\nExpiry = 0.084,\nStrike = 15500,\nSpot = 15000,\nVol = 0.2,\nDivYld = 0.015, \nr = 0.0015,\npath = " << NumberOfPaths << "\n";
        double MonteCall = EuroMonteCarlo("C", Expiry, Strike, Spot, Vol, DivYld, r, NumberOfPaths);
        double MontePut = EuroMonteCarlo("P", Expiry, Strike, Spot, Vol, DivYld, r, NumberOfPaths);
        cout << "\nMonte-Carlo Call: " << MonteCall << "\n";
        cout << "Monte-Carlo Put: " << MontePut << "\n";

        double TheoreticalCall = EuroAnalytic("C", Expiry, Strike, Spot, Vol, DivYld, r);
        double TheoreticalPut = EuroAnalytic("P", Expiry, Strike, Spot, Vol, DivYld, r);

        cout << "theoretical Call: " << TheoreticalCall << "\n";
        cout << "theoretical Put: " << TheoreticalPut << "\n";

        double MonteCminusP = MonteCall - MontePut;
        double TheoreticalCminusP = TheoreticalCall - TheoreticalPut;
        double ForwardPrice = exp((r-DivYld)*Expiry)*Spot - Strike;
        double MontePutCallParity = MonteCminusP - exp(-r*Expiry)*ForwardPrice;
        double TheoreticalPutCallParity = TheoreticalCminusP - exp(-r*Expiry)*ForwardPrice;

        cout << "Monte-Carlo put-call parity:\n C - P - D*(F-K) = " << MontePutCallParity << "\n";
        cout << "Theoretical put-call parity:\n C - P - D*(F-K) = " << TheoreticalPutCallParity << "\n";
    } else {
        cout << "\nEnter expiry\n";
        cin >> Expiry;

        cout << "\nEnter strike\n";
        cin >> Strike;

        cout << "\nEnter spot\n";
        cin >> Spot;

        cout << "\nEnter vol\n";
        cin >> Vol;

        cout << "\nEnter DivYld\n";
        cin >> DivYld;

        cout << "\nr\n";
        cin >> r;

        cout << "\nnumber of paths\n";
        cin >> NumberOfPaths;

        double result = EuroMonteCarlo(PutOrCall,
                                       Expiry,
                                       Strike,
                                       Spot,
                                       Vol,
                                       DivYld,
                                       r,
                                       NumberOfPaths);
        cout << "\nthe price is " << result << "\n"; // 1,100,100,0.02,0.01だと89.5938

        double TheoreticalPrice = EuroAnalytic(PutOrCall,
                                               Expiry,
                                               Strike,
                                               Spot,
                                               Vol,
                                               DivYld,
                                               r);

        cout << "theoretical price is " << TheoreticalPrice << "\n";

        double CallMinusPut = EuroMonteCarlo("C",Expiry,Strike,Spot,Vol,DivYld,r,NumberOfPaths) - EuroMonteCarlo("P",Expiry,Strike,Spot,Vol,DivYld,r,NumberOfPaths);
        double StMunuseK = exp(-DivYld*Expiry)*Spot - exp(-r*Expiry)*Strike;
        double PutCallParity = CallMinusPut - StMunuseK;

        cout << "PutCallParity\n = call - put - e^{-qT}S0 + e^{-rT}K\n = " << PutCallParity << "\n";
    }

    return 0;
}
