import "./erc20.spec"

using DummyERC20A as stakingToken
using DummyERC20B as rewardsToken
/**************************************************
 *              METHODS DECLARATIONS              *
 **************************************************/
methods{
    stakingToken()                  returns (address)   envfree
    rewardsToken()                  returns (address)   envfree
    owner()                         returns (address)   envfree
    duration()                      returns (uint256)   envfree
    finishAt()                      returns (uint256)   envfree
    updatedAt()                     returns (uint256)   envfree
    rewardRate()                    returns (uint256)   envfree
    rewardPerTokenStored()          returns (uint256)   envfree
    userRewardPerTokenPaid(address) returns (uint256)   envfree
    rewards(address)                returns (uint256)   envfree
    totalSupply()                   returns (uint256)   envfree
    balanceOf(address)              returns (uint256)   envfree
    _min(uint256, uint256)          returns(uint256)    envfree
    rewardsToken.balanceOf(address) returns (uint256)   envfree
    stakingToken.balanceOf(address) returns (uint256)   envfree
    updateRewardHelper(address)     envfree
    lastTimeRewardApplicable()      returns (uint256)
    rewardPerToken()                returns (uint256)
    earned(address)                 returns uint256
    stake(uint256)
    withdraw(uint256)
    getReward(address)
    setRewardsDuration(uint256)
    notifyRewardAmount(uint256)
}


// rule sanity(env e, method f){
//     calldataarg args;
//     f(e,args);
//     assert false;
// }

// rule whoChangedDuration(method f, env e){
//     uint256 _duration = duration();
//     calldataarg args;
//     f(e, args);
//     uint256 duration_ = duration();
//     assert e.msg.sender!=owner() => _duration == duration_;
// }
// rule integrityOfStake(){
//     env e;uint256 amount;
//     uint256 _balance=balanceOf(e.msg.sender);
//     stake(e,amount);
//     uint256 balance_=balanceOf(e.msg.sender);
//     assert balance_==_balance+amount;
// }
// rule integrityOfWithdraw(){
//     env e;uint256 amount;
//     uint256 _balance=balanceOf(e.msg.sender);
//     withdraw(e,amount);
//     uint256 balance_=balanceOf(e.msg.sender);
//     assert balance_==_balance-amount;
// }


//  ghost mathint totalRewardBalance{
//   init_state axiom totalRewardBalance == 0;
//   }
//  hook Sstore rewards[KEY address addr] uint new_reward (uint256 old_reward) STORAGE {
//     totalRewardBalance = totalRewardBalance + new_reward - old_reward;
//  }

//  //FAILED :- invariant for ensuring the protocol is not insolvent and always has enough reward Token.
// invariant hasEnoughRewardToken()
//     totalRewardBalance<= rewardsToken.balanceOf(currentContract){
//         preserved with (env e){
//             require e.block.timestamp == updatedAt();
//         }
//     }


// finishAt() >= updatedAt() <= block.timestamp
// invariant finishAtAheadOfUpdateAt()
//     finishAt() >=updatedAt()

// invariant updateAtLessThanBlockTimestamp(uint256 time)
//     updatedAt()<=time
//     {
//     preserved with (env e) {
//         require e.block.timestamp == time;
//     }
//     }


// user reawrd balance can either increase or become 0 . It cannot decrease
// rule userRewardBalanceCannotDecrease(){
//     address user;env e;calldataarg args;method f;

//     uint256 _userBalance = rewards(user);
//     f(e,args);
//     uint256 userBalance_ = rewards(user);

//     assert userBalance_ >= _userBalance || userBalance_==0;
// }

// for same period increase in rewards of two distinct user with same balance (staked balance) must be equal.

rule rewardBalanceEqualIncrement(){
    address user1;address user2; env e;method f;calldataarg args;
    require(user1!=user2);
    require(balanceOf(user1)==balanceOf(user2));

    uint256 _user1_rewards= rewards(user1);
    uint256 _user2_rewards= rewards(user2);

    f(e,args);
    updateRewardHelper(user1);
    updateRewardHelper(user2);

    uint256 user1_rewards_= rewards(user1);
    uint256 user2_rewards_= rewards(user2);

    assert balanceOf(user1)==balanceOf(user2) && (user1_rewards_!=0 && user2_rewards_!=0)  => user1_rewards_ - _user1_rewards == user2_rewards_ - _user2_rewards;

}