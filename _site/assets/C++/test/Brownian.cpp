#include <iostream>
#include <string>
#include <cstdlib>
#include <cmath>
#include <random>

using namespace std;


double EuroCallAnalytic(double Expiry,  // 満期T
                        double Strike,  // 権利行使価格K
                        double Spot,  // 現時点t=0での原資産価格S_0
                        double Vol,  // ボラティリティσ
                        double r  // 金利r
) {
    double logTerm = log( Spot / Strike );
    double thisD1 = ( logTerm + r*Expiry + 0.5*Vol*Vol*Expiry ) / Vol*sqrt(Expiry);
    double thisD2 = thisD1 - Vol*sqrt(Expiry);

    double firstTerm = 0.5*Spot*( 1+erf(thisD1 / sqrt(2)));
    double secondTerm = 0.5*Strike*exp(-r*Expiry)*( 1+erf(thisD2 / sqrt(2)));

    return firstTerm - secondTerm;
}


double EuroMonteCarlo(string PutOrCall,  // putかcallか
                      double Expiry,  // 満期T
                      double Strike,  // 権利行使価格K
                      double Spot,  // 現時点t=0での原資産価格S_0
                      double Vol,  // ボラティリティσ
                      double r,  // 金利r
                      unsigned long NumberOfPaths) {
    double Variance = Vol*Vol*Expiry;  // 分散
    double ItoCorrection = -0.5*Variance;  // -σ^2T/2

    double RootExpiry = sqrt(Expiry);  // √T

    random_device seed_gen;
    default_random_engine generator(seed_gen());
    normal_distribution<double> Wiener(0,Expiry);  // W_Tの分布はN(0,T)

    double movedSpot = Spot*exp(r*Expiry + ItoCorrection);  // S_0exp(T(r-σ^2/2))
    double thisSpot;
    double runningSum=0;

    for (unsigned long i=0; i < NumberOfPaths; i++) {
        double thisGaussian = Wiener(generator);
        thisSpot = movedSpot*exp(thisGaussian);  // S_0exp(σ*W_T + T(r-σ^2/2))
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
    mean *= exp(-r*Expiry);  // 求めたいのはexp(-rT)E[S_0exp(σ*W_T + T(r-σ^2/2))]なので現在価値に換算
    return mean;
}



int main()
{
    string PutOrCall;
    double Expiry;
    double Strike;
    double Spot;
    double Vol;
    double r;
    unsigned long NumberOfPaths;

    cout << "\nPut or Call\n";
    cin >> PutOrCall;

    cout << "\nEnter expiry\n";
    cin >> Expiry;

    cout << "\nEnter strike\n";
    cin >> Strike;

    cout << "\nEnter spot\n";
    cin >> Spot;

    cout << "\nEnter vol\n";
    cin >> Vol;

    cout << "\nr\n";
    cin >> r;

    cout << "\nnumber of paths\n";
    cin >> NumberOfPaths;
    double result = EuroMonteCarlo(PutOrCall,
                                   Expiry,
                                   Strike,
                                   Spot,
                                   Vol,
                                   r,
                                   NumberOfPaths);
    cout << "\nthe price is " << result << "\n"; // 1,100,100,0.02,0.01だと89.5938

    double TheoreticalPrice = EuroCallAnalytic(Expiry,
                                               Strike,
                                               Spot,
                                               Vol,
                                               r);

    cout << "theoretical price is " << TheoreticalPrice << "\n";

    double CallMinusPut = EuroMonteCarlo("C",Expiry,Strike,Spot,Vol,r,NumberOfPaths) - EuroMonteCarlo("P",Expiry,Strike,Spot,Vol,r,NumberOfPaths);
    double StMunuseK = Spot - exp(-r*Expiry)*Strike;
    double PutCallParity = CallMinusPut - StMunuseK;

    cout << "\ncall - put - S0 + e^{-rT}K = " << PutCallParity << "\n";

    return 0;
}
