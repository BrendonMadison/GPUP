
 using namespace std;
 using namespace RooFit;
 using namespace RooStats;
 
 
void MultivariateGaussian(string bfile="electron.ini",unsigned int seed=1,Double_t Espread = 0.00190, Double_t corr = 0.3, Double_t Emean = 125.0, 
               Double_t meanZ = 0.0, Double_t truncate = 4.0 , 
	       Int_t N = 80000, Double_t sigmaZ=300.0, Double_t betaX=13.0, 
               Double_t betaY=0.41, Double_t emittX=5.0, Double_t emittY=0.035)
 {
    // Open output file
    ofstream beamfile;
    beamfile.open(bfile);
    
	//Some computations
	
    const Double_t m=0.5109989461e-3;
	Double_t gamma = Emean/m;
    Double_t sigmaE  = Espread*Emean;
	
	
// Use the transverse beam emittance and beta functions to calculate 
// transverse beam-size and divergence assuming no correlations 
//
// Input normalized emittances and beta parameters are in the same units as Guinea-PIG input, 
// namely emittance (10^-6 m. rad) and beta (mm)
//  
// Convert to SI units of m.rad and m
    Double_t bX = betaX*1.0e-3;
    Double_t bY = betaY*1.0e-3;
    Double_t eX = emittX*1.0e-6;
    Double_t eY = emittY*1.0e-6;
// Conversion factor from meters to microns and and radians to micro-radians
    const Double_t CONV=1.0e6;
    Double_t sigmaX  = CONV*sqrt(eX*bX/gamma);
    Double_t sigmaY  = CONV*sqrt(eY*bY/gamma);
    Double_t sigmaXP = CONV*sqrt(eX/(gamma*bX));
    Double_t sigmaYP = CONV*sqrt(eY/(gamma*bY));	
	//Declare your variables
    RooArgList xVec;
    RooArgList muVec;
	
    RooRealVar* x;
    RooRealVar* mu_x;

    //Set the variables and their ranges.
    RooRealVar Ex("Energy", "Energy", Emean, Emean-truncate*sigmaE,Emean+truncate*sigmaE);
	RooRealVar Xx("x","x",0.0,0.0-truncate*sigmaX,0.0+truncate*sigmaX);
	RooRealVar Yx("y","y",0.0,0.0-truncate*sigmaY,0.0+truncate*sigmaY);
	RooRealVar Zx("z","z",meanZ,meanZ-truncate*sigmaZ,meanZ+truncate*sigmaZ);
    RooRealVar Xp("px","px",0.0,0.0-truncate*sigmaXP,meanZ+truncate*sigmaXP);
	RooRealVar Yp("py","py",0.0,0.0-truncate*sigmaYP,meanZ+truncate*sigmaYP);
	xVec.add(Ex);
    xVec.add(Xx);
	xVec.add(Yx);
	xVec.add(Zx);
	xVec.add(Xp);
	xVec.add(Yp);

    RooRealVar mu_E("mu_E", "mu_E", Emean, Emean,Emean);
    RooRealVar mu_X("mu_x", "mu_x", 0.0, 0.0,0.0);
	RooRealVar mu_Y("mu_y", "mu_y", 0.0, 0.0,0.0);
	RooRealVar mu_Z("mu_z", "mu_z", meanZ, meanZ,meanZ);
	RooRealVar mu_Xp("mu_px", "mu_px", 0.0, 0.0,0.0);
	RooRealVar mu_Yp("mu_py", "mu_py", 0.0, 0.0,0.0);
	muVec.add(mu_E);
    muVec.add(mu_X);
	muVec.add(mu_Y);
	muVec.add(mu_Z);
	muVec.add(mu_Xp);
	muVec.add(mu_Yp);
	
 
    // make a covariance matrix with the variance and correlation values
    TMatrixDSym cov(6);
	//Fill the matrix with zeros
	for (int i=0;i<6;i++){
		for (int j=0;j<6;j++){
			cov(i,j) = 0;
		}
	}

	//Set the variances (std dev)
	cov(0,0) = sigmaE*sigmaE;
	cov(1,1) = sigmaX*sigmaX;
	cov(2,2) = sigmaY*sigmaY;
	cov(3,3) = sigmaZ*sigmaZ;
	cov(4,4) = sigmaXP*sigmaXP;
	cov(5,5) = sigmaYP*sigmaYP;

	//Add the non-zero correlations
	cov(3,0) = corr*sigmaE*sigmaZ;
	cov(0,3) = corr*sigmaE*sigmaZ;
    	
    // now make the multivariate Gaussian
    RooMultiVarGaussian mvg("mvg", "mvg", xVec, muVec, cov);
 
    // --------------------
    // make a toy dataset
    RooDataSet* data = mvg.generate(xVec, N);

    //Write dataset to file
    data->write(bfile.c_str());
	beamfile.close();

	//Call system to execute a shell command to sort the file according to ordering z
	system(Form("sort -g --key=4 %s > %s",bfile.c_str(),"temp.tmp"));
        system(Form("mv temp.tmp %s",bfile.c_str()));	
 }
