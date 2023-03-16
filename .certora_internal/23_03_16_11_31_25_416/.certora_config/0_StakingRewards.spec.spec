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
rule integrityOfStake(){
    env e;uint256 amount;
    require(e.msg.sender!=currentContract);

    uint256 _balance=balanceOf(e.msg.sender);
    uint256 _totalSupply = totalSupply();
    uint256 _userTokenBalance=stakingToken.balanceOf(e.msg.sender);

    stake(e,amount);

    uint256 balance_=balanceOf(e.msg.sender);
    uint256 totalSupply_ = totalSupply();
     uint256 userTokenBalance_=stakingToken.balanceOf(e.msg.sender);

    assert balance_==_balance+amount;
    assert totalSupply_ == _totalSupply + amount;
    assert userTokenBalance_==_userTokenBalance-amount;
}
rule integrityOfWithdraw(){
    env e;uint256 amount;
        require(e.msg.sender!=currentContract);

    uint256 _balance=balanceOf(e.msg.sender);
    uint256 _totalSupply = totalSupply();
    uint256 _userTokenBalance=stakingToken.balanceOf(e.msg.sender);

    withdraw(e,amount);

    uint256 balance_=balanceOf(e.msg.sender);
    uint256 totalSupply_ = totalSupply();
     uint256 userTokenBalance_=stakingToken.balanceOf(e.msg.sender);

    assert balance_==_balance-amount;
    assert amount <= _balance;
    assert totalSupply_== _totalSupply-amount;
    assert userTokenBalance_ == _userTokenBalance +amount;
}

rule getRewardIntegrity(){
    env e;
        require(e.msg.sender!=currentContract);
    uint256 _user_reward_token_balance=rewardsToken.balanceOf(e.msg.sender);
    uint256 _user_reward_balance = rewards(e.msg.sender);

    getReward(e);

    uint256 user_reward_token_balance_=rewardsToken.balanceOf(e.msg.sender);
    uint256 user_reward_balance_ = rewards(e.msg.sender);

    assert user_reward_balance_ ==0 && user_reward_token_balance_== _user_reward_token_balance + _user_reward_balance;

}
rule onlyGetRewardDecreaseRewardBalance(){
    address user;env e;method f;calldataarg args;

    uint256 _balance=rewards(user);

    f(e,args);

    uint256 balance_=rewards(user);

    assert balance_ < _balance => f.selector == getReward().selector;
}

// reduction of staked balance should only be possible with withdraw function

rule onlyWithdrawDecreaseBalance(){
    address user;env e;method f;calldataarg args;
    uint256 _balance = balanceOf(user);
    f(e,args);
    uint256 balance_ = balanceOf(user);

    assert balance_ < _balance => f.selector == withdraw(uint256).selector;

}

// increment of staked balance should only be possible with deposit function.
rule onlyDepositIncreaseBalance(){
    address user;env e;method f;calldataarg args;
    uint256 _balance = balanceOf(user);
    f(e,args);
    uint256 balance_ = balanceOf(user);

    assert balance_ > _balance => f.selector == stake(uint256).selector;

}


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

// two user staking same amount at same time  should yield same rewards

rule rewardBalanceEqualIncrement(){
    address user1;address user2;env e; env e1;env e2;env e3;method f;calldataarg args;uint256 amount;
    require(e1.block.timestamp == e2.block.timestamp && e1.msg.sender!=e2.msg.sender);
   
    uint256 _user1_rewards= rewards(e1.msg.sender);
    uint256 _user2_rewards= rewards(e2.msg.sender);

    stake(e1,amount);
    stake(e2,amount);


    require(e3.block.timestamp > e1.block.timestamp);

    uint256 user1_rewards_=earned(e3,e1.msg.sender);
    uint256 user2_rewards_= earned(e3,e2.msg.sender);

    assert user1_rewards_ - _user1_rewards == user2_rewards_ - _user2_rewards;
}

